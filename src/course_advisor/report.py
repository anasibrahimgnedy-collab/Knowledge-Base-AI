"""Render plans as Markdown / JSON for the test report and the notebook."""
from __future__ import annotations

from .models import Decision, Hit, Plan, Verdict

MAX_REJECTED_SHOWN = 10
MAX_REJECTED_EVIDENCE = 5


def cite(hit: Hit) -> str:
    c = hit.chunk
    return f"{c.source_file} § {c.section}"


def quote(hit: Hit, width: int = 260) -> str:
    text = hit.chunk.text if len(hit.chunk.text) <= width else hit.chunk.text[:width].rsplit(" ", 1)[0] + " …"
    return f"> **[{cite(hit)}]** (sim {hit.score:.2f}) {text}"


def rejected_for_display(plan: Plan) -> list[Decision]:
    """Rejected courses worth showing: requested ones first, then most relevant / closest to eligibility."""
    items = [d for d in plan.decisions.values() if d.verdict is Verdict.REJECTED]
    requested = set(plan.profile.requested_courses)
    items.sort(key=lambda d: (d.course_code not in requested, len(d.violations), -d.relevance, d.course_code))
    keep = [d for d in items if d.course_code in requested]
    keep += [d for d in items if d.course_code not in requested][:MAX_REJECTED_SHOWN]
    return keep


def plan_markdown(plan: Plan, courses: dict) -> str:
    p = plan.profile
    out = [f"# Test Profile: {p.name}", ""]
    if p.description:
        out += [f"**Scenario:** {p.description}", ""]
    out += ["## 1. Student input", "",
            "| Field | Value |", "|---|---|",
            f"| Academic level | {p.level} |", f"| Upcoming term | {p.term} |",
            f"| GPA | {p.gpa if p.gpa is not None else 'none (first semester)'} |",
            f"| Passed courses | {', '.join(p.passed_courses) or 'none'} |",
            f"| Skills | {', '.join(p.skills) or '-'} |", f"| Interests | {', '.join(p.interests) or '-'} |",
            f"| Goals | {p.goals or '-'} |", f"| Preferred credit load | {p.preferred_credits} |",
            f"| Requested courses | {', '.join(p.requested_courses) or '-'} |", ""]

    shown_rejected = rejected_for_display(plan)
    out += ["## 2. Retrieved evidence from the Knowledge Base", "",
            "### 2a. Course passages (retrieved per course)", ""]
    shown = [plan.decisions[c] for c in plan.selected] + shown_rejected
    for d in shown[:len(plan.selected) + MAX_REJECTED_EVIDENCE]:
        out.append(f"**{d.course_code} ({d.verdict.value})**")
        out += [quote(h) for h in d.evidence]
        out.append("")
    policy_hits: dict[str, Hit] = {}
    for h in plan.policy_evidence.get("CREDIT_LIMIT_EXCEEDED", []):
        policy_hits[h.chunk.chunk_id] = h
    for d in shown:
        for h in d.policy_evidence:
            policy_hits[h.chunk.chunk_id] = h
    out += ["### 2b. Policy passages (retrieved for the rules applied)", "",
            f"Credit limit for this student: {plan.max_credits} credit hours.", ""]
    out += [quote(h, 400) + "\n" for h in policy_hits.values()]

    out += ["## 3. Accepted courses", "",
            "| Course | Title | Credits | Reasons |", "|---|---|---|---|"]
    for code in plan.selected:
        c, d = courses[code], plan.decisions[code]
        out.append(f"| {code} | {c.title} | {c.credits} | {' '.join(d.reasons)} |")
    out.append("")

    out += ["## 4. Rejected courses and reasons", "",
            "| Course | Title | Rule failed | Reason | Policy source |", "|---|---|---|---|---|"]
    for d in shown_rejected:
        title = courses[d.course_code].title if d.course_code in courses else "(unknown)"
        rules = ", ".join(v.rule.value for v in d.violations)
        why = "; ".join(v.message for v in d.violations)
        src = "; ".join(sorted({cite(h) for h in d.policy_evidence}))
        hint = f" **Hint:** {' '.join(d.reasons)}" if d.reasons else ""
        out.append(f"| {d.course_code} | {title} | {rules} | {why}.{hint} | {src} |")
    n_hidden = sum(1 for d in plan.decisions.values() if d.verdict is Verdict.REJECTED) - len(shown_rejected)
    if n_hidden > 0:
        out.append(f"\n_({n_hidden} further courses are also ineligible; see the JSON output for the full list.)_")
    notsel = plan.by_verdict(Verdict.ELIGIBLE_NOT_SELECTED)[:5]
    if notsel:
        out += ["", "Eligible but not selected (would exceed the planned load):",
                ", ".join(f"{d.course_code} ({courses[d.course_code].credits} cr)" for d in notsel)]
    out.append("")

    out += ["## 5. Final recommendation", "",
            f"**Register for:** {', '.join(plan.selected) or 'none'}  ",
            f"**Total:** {plan.total_credits} credit hours "
            f"(maximum allowed: {plan.max_credits}, planned: {plan.target_credits})", ""]
    for w in plan.warnings:
        out.append(f"- WARNING: {w}")
    return "\n".join(out) + "\n"


def plan_dict(plan: Plan) -> dict:
    return {
        "student": plan.profile.name, "label": plan.label,
        "max_credits": plan.max_credits, "target_credits": plan.target_credits,
        "total_credits": plan.total_credits, "selected": plan.selected, "warnings": plan.warnings,
        "decisions": {
            code: {"verdict": d.verdict.value, "score": round(d.score, 3),
                   "violations": [{"rule": v.rule.value, "message": v.message} for v in d.violations],
                   "reasons": d.reasons,
                   "evidence": [{"source": cite(h), "score": round(h.score, 3), "text": h.chunk.text}
                                for h in [*d.evidence, *d.policy_evidence]]}
            for code, d in sorted(plan.decisions.items())},
    }


def plan_summary(plan: Plan, courses: dict) -> str:
    lines = [f"{plan.label}: {plan.total_credits}/{plan.max_credits} credit hours"]
    lines += [f"  - {c} {courses[c].title} ({courses[c].credits} cr)" for c in plan.selected]
    return "\n".join(lines)
