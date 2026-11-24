"""Conversational layer: intent handling is deterministic; the LLM only phrases replies."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field, replace

from .llm import SYSTEM_PROMPT, LLMClient
from .models import Plan, StudentProfile, Verdict
from .recommender import Advisor
from .report import cite, plan_summary

log = logging.getLogger(__name__)
CODE_RE = re.compile(r"\b([A-Za-z]{2,4}\d{3}L?)\b")


@dataclass
class ChatReply:
    text: str
    sources: list[str] = field(default_factory=list)
    used_llm: bool = False


class AdvisorChat:
    def __init__(self, advisor: Advisor, profile: StudentProfile, llm: LLMClient | None = None) -> None:
        self.advisor = advisor
        self.profile = replace(profile)
        self.llm = llm
        self.plan: Plan = advisor.plan(self.profile)

    # -------------------------------------------------------------- public
    def handle(self, message: str) -> ChatReply:
        text = message.strip()
        low = text.lower()
        codes = [c.upper() for c in CODE_RE.findall(text)]
        if not text:
            return ChatReply("Please type a question or a preference change.")
        if re.search(r"\b(why|explain|reason)\b", low) and codes:
            return self._explain(codes[0], text)
        if re.search(r"\b(alternative|other plan|different plan|options)\b", low):
            return self._alternatives(text)
        changed = self._apply_changes(text, low, codes)
        if changed:
            self.plan = self.advisor.plan(self.profile)
            return self._finish("Preferences updated: " + "; ".join(changed) + ".\n" + self._plan_text(),
                                text, self._plan_sources())
        if re.search(r"\b(plan|recommend|register|schedule|show)\b", low):
            return self._finish(self._plan_text(), text, self._plan_sources())
        return self._answer_from_kb(text)

    # ------------------------------------------------------------- intents
    def _apply_changes(self, text: str, low: str, codes: list[str]) -> list[str]:
        changes = []
        m = re.search(r"(\d{1,2})\s*(?:credit|credits|credit hours|hours)\b", low)
        if m and re.search(r"\b(want|prefer|take|load|plan|make|only)\b", low):
            self.profile.preferred_credits = int(m.group(1))
            changes.append(f"preferred load set to {m.group(1)} credit hours")
        elif re.search(r"\b(lighter|lighter load|easier|fewer courses)\b", low):
            self.profile.preferred_credits = self.advisor.rules.policy.min_full_time
            changes.append(f"preferred load set to {self.profile.preferred_credits} credit hours")
        m = re.search(r"(?:interested in|i like|i love|add interest(?: in)?)\s+(.+?)(?:[.!?]|$)", low)
        if m:
            self.profile.interests.append(m.group(1).strip())
            changes.append(f"added interest '{m.group(1).strip()}'")
        if codes and re.search(r"\b(add|take|want|include|register)\b", low) and not m:
            for c in codes:
                if c not in self.profile.requested_courses:
                    self.profile.requested_courses.append(c)
                    changes.append(f"requested {c}")
        if codes and re.search(r"\b(remove|drop|skip|don't want|do not want)\b", low):
            for c in codes:
                if c in self.profile.requested_courses:
                    self.profile.requested_courses.remove(c)
                    changes.append(f"removed request for {c}")
        return changes

    def _explain(self, code: str, question: str) -> ChatReply:
        d = self.plan.decisions.get(code)
        course = self.advisor.courses.get(code)
        if d is None or course is None:
            return ChatReply(f"I could not find {code} in the knowledge base.")
        if d.verdict is Verdict.ALREADY_PASSED:
            text = f"{code} ({course.title}) is already passed, so it cannot be registered again."
        elif d.verdict is Verdict.REJECTED:
            text = (f"{code} ({course.title}) is NOT allowed: " + "; ".join(v.message for v in d.violations)
                    + f" [{', '.join(sorted({cite(h) for h in (*d.evidence, *d.policy_evidence)}))}]")
        elif d.verdict is Verdict.RECOMMENDED:
            text = f"{code} ({course.title}) is recommended. " + " ".join(d.reasons)
        else:
            text = (f"{code} ({course.title}) is eligible but was not selected. " + " ".join(d.reasons)
                    + " Ask for a different load or add it explicitly.")
        return self._finish(text, question, [cite(h) for h in (*d.evidence, *d.policy_evidence)])

    def _alternatives(self, question: str) -> ChatReply:
        plans = self.advisor.alternatives(self.profile)
        text = "Here are alternative semester plans:\n" + "\n".join(
            plan_summary(p, self.advisor.courses) for p in plans)
        if len(plans) == 1:
            text += ("\nNo different plan exists: every other rule-compliant combination uses the same courses. "
                     "Try raising the preferred load, changing interests, or requesting a specific course.")
        return self._finish(text, question, [])

    def _answer_from_kb(self, question: str) -> ChatReply:
        hits = self.advisor.retriever.retrieve(question, 3)
        if not hits:
            return ChatReply("I could not find anything about that in the knowledge base.")
        text = "From the knowledge base:\n" + "\n".join(f"- [{cite(h)}] {h.chunk.text}" for h in hits)
        return self._finish(text, question, [cite(h) for h in hits])

    # --------------------------------------------------------------- output
    def _plan_text(self) -> str:
        p = self.plan
        lines = [f"Recommended plan for {p.profile.name} ({p.total_credits}/{p.max_credits} credit hours):"]
        for code in p.selected:
            c = self.advisor.courses[code]
            lines.append(f"- {code} {c.title} ({c.credits} cr): {' '.join(p.decisions[code].reasons[:2])}")
        lines += [f"WARNING: {w}" for w in p.warnings]
        return "\n".join(lines)

    def _plan_sources(self) -> list[str]:
        return sorted({cite(h) for d in self.plan.decisions.values()
                       if d.verdict is Verdict.RECOMMENDED for h in d.evidence[:1]})

    def _finish(self, grounded: str, question: str, sources: list[str]) -> ChatReply:
        """Let the LLM rephrase the grounded text; fall back if it strays from the facts."""
        if self.llm is None:
            return ChatReply(grounded, sources)
        prompt = f"FACTS:\n{grounded}\n\nSTUDENT QUESTION: {question}"
        try:
            answer = self.llm.complete(SYSTEM_PROMPT, prompt)
        except Exception as exc:  # network/API failure must not break advising
            log.warning("LLM call failed (%s); using grounded template", exc)
            return ChatReply(grounded, sources)
        allowed = {c.upper() for c in CODE_RE.findall(grounded)}
        mentioned = {c.upper() for c in CODE_RE.findall(answer)}
        if not mentioned <= allowed:
            log.warning("LLM mentioned ungrounded courses %s; using template", sorted(mentioned - allowed))
            return ChatReply(grounded, sources)
        return ChatReply(answer, sources, used_llm=True)
