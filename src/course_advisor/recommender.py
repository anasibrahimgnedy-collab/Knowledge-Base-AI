"""Recommendation engine: rule engine + retrieval + ranking + credit-limit packing."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, replace

from . import config
from .knowledge_base import build_courses, build_credit_policy, chunk_documents, load_documents
from .models import Course, Decision, Hit, Plan, RuleId, StudentProfile, Verdict, Violation
from .retriever import Retriever
from .rules import RuleEngine

log = logging.getLogger(__name__)

# Natural-language queries used to retrieve the policy passage backing each rule.
RULE_QUERIES = {
    RuleId.ALREADY_PASSED: "student may not register again for a course that has already been passed",
    RuleId.NOT_OFFERED: "semester availability course offered Fall Spring",
    RuleId.LEVEL: "academic level restriction register courses at or below the student level",
    RuleId.PREREQ: "student may register for a course only if every prerequisite listed has been passed",
    RuleId.MIN_CREDITS: "minimum passed credit hours required for senior courses",
    RuleId.MIN_GPA: "minimum cumulative GPA requirement for registration",
    RuleId.COREQ: "corequisite registered in the same semester",
    RuleId.CREDIT_LIMIT: "maximum credit hours per semester based on GPA exceeding the limit",
}


@dataclass(frozen=True)
class Weights:
    relevance: float = config.WEIGHT_RELEVANCE
    core: float = config.WEIGHT_CORE
    at_level: float = config.WEIGHT_AT_LEVEL
    requested: float = config.WEIGHT_REQUESTED


PRESETS = {
    "balanced": Weights(),
    "core_first": Weights(relevance=0.5, core=1.0),
    "interest_first": Weights(relevance=1.5, core=0.1, at_level=0.05),
}


class Advisor:
    """Facade that wires the knowledge base, retriever and rule engine together."""

    def __init__(self, retriever: Retriever, rules: RuleEngine) -> None:
        self.retriever = retriever
        self.rules = rules
        self.courses = rules.courses

    @classmethod
    def from_knowledge_base(cls, embedder=None) -> Advisor:
        docs = load_documents()
        chunks = chunk_documents(docs)
        courses = build_courses(docs)
        rules = RuleEngine(courses, build_credit_policy(docs))
        log.info("Knowledge base: %d courses, %d chunks", len(courses), len(chunks))
        return cls(Retriever(chunks, embedder), rules)

    # ------------------------------------------------------------------
    def plan(self, profile: StudentProfile, *, preset: str = "balanced",
             target_override: int | None = None, label: str | None = None) -> Plan:
        self.rules.validate_profile(profile)
        weights = PRESETS[preset]
        max_credits, basis = self.rules.max_credits(profile)
        wanted = target_override or profile.preferred_credits
        target = min(wanted, max_credits)
        warnings: list[str] = []
        if wanted > max_credits:
            warnings.append(f"Preferred load of {wanted} credit hours exceeds the maximum of "
                            f"{max_credits} allowed for this student ({basis}); the plan is capped at {max_credits}.")

        relevance = self.retriever.course_relevance(profile.interest_query())
        decisions: dict[str, Decision] = {}
        eligible: list[str] = []
        for code, course in self.courses.items():
            viol = self.rules.violations(profile, code)
            requested = code in profile.requested_courses
            if viol and viol[0].rule is RuleId.ALREADY_PASSED:
                decisions[code] = Decision(code, Verdict.ALREADY_PASSED, viol)
            elif viol:
                decisions[code] = Decision(code, Verdict.REJECTED, viol,
                                           relevance=relevance.get(code, 0.0))
            else:
                score = (weights.relevance * relevance.get(code, 0.0)
                         + (weights.core if course.category == "core" else 0.0)
                         + (weights.at_level if course.level == profile.level else 0.0)
                         + (weights.requested if requested else 0.0))
                decisions[code] = Decision(code, Verdict.ELIGIBLE_NOT_SELECTED, [], [],
                                           score, relevance.get(code, 0.0))
                eligible.append(code)
        for code in profile.requested_courses:
            if code not in self.courses:
                decisions[code] = Decision(code, Verdict.REJECTED, [Violation(
                    RuleId.UNKNOWN_COURSE, f"{code} does not exist in the knowledge base")])

        selected, total = self._pack(profile, decisions, eligible, target, max_credits)
        if total < self.rules.policy.min_full_time:
            warnings.append(f"Plan totals {total} credit hours, below the {self.rules.policy.min_full_time}-credit "
                            f"full-time minimum; too few eligible courses were available.")
        plan = Plan(profile, max_credits, target, selected, total, decisions, warnings,
                    label=label or preset)
        self._attach_evidence(plan, profile)
        return plan

    # ------------------------------------------------------------------
    def _groups(self, p: StudentProfile, eligible: list[str]) -> list[list[tuple[str, ...]]]:
        """Corequisite-linked components, each expressed as its valid course subsets (options).

        A subset is valid when every course in it has its unmet corequisites in the subset too.
        """
        passed = set(p.passed_courses)
        elig = set(eligible)
        parent = {c: c for c in elig}

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for c in elig:
            for co in self.courses[c].corequisites:
                if co in elig and co not in passed:
                    parent[find(c)] = find(co)
        comps: dict[str, list[str]] = {}
        for c in sorted(elig):
            comps.setdefault(find(c), []).append(c)
        groups = []
        for members in comps.values():
            options = []
            for mask in range(1 << len(members)):
                subset = tuple(m for i, m in enumerate(members) if mask >> i & 1)
                if all(co in subset or co in passed
                       for m in subset for co in self.courses[m].corequisites):
                    options.append(subset)
            groups.append(options)
        return groups

    def _knapsack(self, groups, base: set[str], capacity: int, value) -> set[str]:
        """Exact multiple-choice knapsack: best option per group within ``capacity`` credit hours."""
        best: dict[int, tuple[float, tuple[tuple[str, ...], ...]]] = {0: (0.0, ())}
        for options in groups:
            members = {c for o in options for c in o}
            forced = base & members
            new: dict[int, tuple[float, tuple[tuple[str, ...], ...]]] = {}
            for used, (val, picks) in best.items():
                for opt in options:
                    if not forced <= set(opt):
                        continue
                    extra = sum(self.courses[c].credits for c in opt if c not in base)
                    if used + extra > capacity:
                        continue
                    cand = (val + value(opt, base), (*picks, opt))
                    if used + extra not in new or cand[0] > new[used + extra][0]:
                        new[used + extra] = cand
            best = new
        if not best:
            return set()
        top = max(best.values(), key=lambda t: t[0])
        return {c for opt in top[1] for c in opt}

    def _pack(self, p: StudentProfile, decisions: dict[str, Decision], eligible: list[str],
              target: int, max_credits: int) -> tuple[list[str], int]:
        """Choose the plan: requested courses first (within the hard maximum), then fill to the target."""
        credits = lambda c: self.courses[c].credits  # noqa: E731
        groups = self._groups(p, eligible)
        requested = set(p.requested_courses)
        # Phase A - requested courses, best total score within the hard maximum.
        chosen = self._knapsack(
            groups, set(), max_credits,
            lambda opt, base: sum(decisions[c].score for c in opt if c in requested)
            - 1e-6 * sum(credits(c) for c in opt))
        # Phase B - fill the planned load: maximise credit hours (<= target), then course score.
        used = sum(credits(c) for c in chosen)
        chosen = self._knapsack(
            groups, chosen, max(target - used, 0),
            lambda opt, base: sum(1000 * credits(c) + decisions[c].score for c in opt if c not in base))
        selected = sorted(chosen, key=lambda c: (-decisions[c].score, c))
        total = sum(credits(c) for c in selected)
        passed = set(p.passed_courses)
        for code in selected:
            decisions[code].verdict = Verdict.RECOMMENDED
            decisions[code].reasons = self._why(p, self.courses[code], decisions[code], code in requested)
        for code in selected:
            for co in self.courses[code].corequisites:
                if co in selected and co not in passed:
                    decisions[co].reasons.insert(0, f"Corequisite of {code}; must be registered together.")
        for code in eligible:
            if code in chosen:
                continue
            cost = credits(code) + sum(credits(co) for co in self.courses[code].corequisites
                                       if co not in passed and co not in chosen)
            if code in requested:
                decisions[code].verdict = Verdict.REJECTED
                decisions[code].violations.append(Violation(
                    RuleId.CREDIT_LIMIT,
                    f"adding {code} ({cost} credit hours) would bring the load to {total + cost}, "
                    f"above the maximum of {max_credits}"))
            else:
                decisions[code].reasons.append(
                    f"Eligible, but adding it ({cost} credit hours) would exceed the planned load of {target}.")
        return selected, total

    def _why(self, p: StudentProfile, course: Course, d: Decision, requested: bool) -> list[str]:
        reasons = []
        if requested:
            reasons.append("Requested by the student and passes every registration rule.")
        if course.prerequisites:
            reasons.append(f"Prerequisites satisfied: {', '.join(course.prerequisites)} passed.")
        else:
            reasons.append("No prerequisites required.")
        reasons.append(f"Offered in {p.term}; level {course.level} is within student level {p.level}.")
        if course.category == "core":
            reasons.append("Core degree requirement.")
        matched = self.matched_interests(p, course)
        if matched:
            reasons.append(f"Matches your interests/goals: {', '.join(matched)}.")
        return reasons

    def matched_interests(self, p: StudentProfile, course: Course) -> list[str]:
        haystack = " ".join([course.title, *course.tags]).lower()
        words = set(re.findall(r"[a-z]{4,}", haystack))
        out = []
        for phrase in [*p.interests, *p.skills]:
            tokens = set(re.findall(r"[a-z]{4,}", phrase.lower()))
            if tokens & words or phrase.lower() in haystack:
                out.append(phrase)
        return out

    # ------------------------------------------------------------------
    def _attach_evidence(self, plan: Plan, p: StudentProfile) -> None:
        query_cache: dict[RuleId, list[Hit]] = {}

        def policy_hits(rule: RuleId) -> list[Hit]:
            if rule not in query_cache:
                query_cache[rule] = self.retriever.retrieve(RULE_QUERIES[rule], 1, doc_type="policy")
            return query_cache[rule]

        for code, d in plan.decisions.items():
            if code not in self.courses or d.verdict is Verdict.ALREADY_PASSED:
                continue
            show = (d.verdict in (Verdict.RECOMMENDED, Verdict.REJECTED)
                    or code in p.requested_courses)
            if not show:
                continue
            course = self.courses[code]
            d.evidence = self.retriever.retrieve(
                f"{code} {course.title} credit hours level offered prerequisites requirements", 1,
                doc_id=code, section="Overview")
            if d.verdict is Verdict.RECOMMENDED and p.interest_query():
                extra = self.retriever.retrieve(p.interest_query(), 1, doc_id=code)
                d.evidence += [h for h in extra if h.chunk.chunk_id != d.evidence[0].chunk.chunk_id]
            for v in d.violations:
                d.policy_evidence += [h for h in policy_hits(v.rule) if h not in d.policy_evidence]
            if d.verdict is Verdict.REJECTED:
                d.reasons = self._unlock_hints(p, d)
        plan.policy_evidence[RuleId.CREDIT_LIMIT.value] = policy_hits(RuleId.CREDIT_LIMIT)

    def _unlock_hints(self, p: StudentProfile, d: Decision) -> list[str]:
        """Tell the student which missing prerequisites could be taken now."""
        hints = []
        for v in d.violations:
            if v.rule is RuleId.PREREQ:
                missing = [c.strip() for c in v.message.split(":", 1)[1].split(",")]
                ready = [c for c in missing if self.rules.is_eligible(p, c)]
                if ready:
                    hints.append(f"Take {', '.join(ready)} first (eligible now) to work towards {d.course_code}.")
        return hints

    # ------------------------------------------------------------------
    def alternatives(self, profile: StudentProfile) -> list[Plan]:
        """Primary plan plus distinct alternatives (different emphasis, lighter load)."""
        plans = [self.plan(profile, preset="balanced", label="balanced")]
        candidates = [
            ("core_first", None, "core-first"),
            ("interest_first", None, "interest-first"),
            ("balanced", self.rules.policy.min_full_time, "lighter load"),
        ]
        seen = {tuple(sorted(plans[0].selected))}
        for preset, target, label in candidates:
            alt = self.plan(replace(profile), preset=preset, target_override=target, label=label)
            key = tuple(sorted(alt.selected))
            if key not in seen and alt.selected:
                seen.add(key)
                plans.append(alt)
        return plans
