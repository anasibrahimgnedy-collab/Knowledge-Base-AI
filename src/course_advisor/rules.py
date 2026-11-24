"""Deterministic academic rule engine.

No LLM or retrieval is involved here: every verdict is computed from the
structured fields parsed out of the knowledge-base documents.
"""
from __future__ import annotations

from . import config
from .models import Course, CreditPolicy, RuleId, StudentProfile, Violation


class ProfileError(ValueError):
    """Raised for an invalid student profile."""


class RuleEngine:
    def __init__(self, courses: dict[str, Course], policy: CreditPolicy) -> None:
        self.courses = courses
        self.policy = policy

    # ---- profile -------------------------------------------------------
    def validate_profile(self, p: StudentProfile) -> None:
        if p.level not in (1, 2, 3, 4):
            raise ProfileError(f"{p.name}: academic level must be 1-4, got {p.level}")
        if p.term not in config.VALID_TERMS:
            raise ProfileError(f"{p.name}: term must be one of {config.VALID_TERMS}")
        if p.gpa is not None and not 0.0 <= p.gpa <= 4.0:
            raise ProfileError(f"{p.name}: GPA must be between 0.0 and 4.0")
        if p.preferred_credits <= 0:
            raise ProfileError(f"{p.name}: preferred credits must be positive")
        unknown = [c for c in p.passed_courses if c not in self.courses]
        if unknown:
            raise ProfileError(f"{p.name}: unknown passed course codes {unknown}")

    def passed_credits(self, p: StudentProfile) -> int:
        return sum(self.courses[c].credits for c in set(p.passed_courses))

    # ---- credit limit --------------------------------------------------
    def max_credits(self, p: StudentProfile) -> tuple[int, str]:
        """Return (limit, human-readable basis) per the credit-load policy."""
        pol = self.policy
        if p.gpa is None:
            return pol.max_first_semester, "no GPA yet (first-semester limit)"
        if p.gpa < pol.gpa_probation_below:
            return pol.max_probation, f"GPA {p.gpa:.2f} < {pol.gpa_probation_below} (probation limit)"
        if p.gpa >= pol.gpa_honors_from:
            return pol.max_honors, f"GPA {p.gpa:.2f} >= {pol.gpa_honors_from} (honors limit)"
        return pol.max_standard, f"GPA {p.gpa:.2f} (standard limit)"

    # ---- per-course eligibility ---------------------------------------
    def violations(self, p: StudentProfile, code: str, *, check_coreq: bool = True) -> list[Violation]:
        course = self.courses.get(code)
        if course is None:
            return [Violation(RuleId.UNKNOWN_COURSE, f"{code} does not exist in the knowledge base")]
        passed = set(p.passed_courses)
        out: list[Violation] = []
        if code in passed:
            return [Violation(RuleId.ALREADY_PASSED, f"{code} has already been passed")]
        if p.term not in course.offered:
            out.append(Violation(RuleId.NOT_OFFERED,
                                 f"{code} is offered only in {' and '.join(course.offered)}, not in {p.term}"))
        if course.level > p.level:
            out.append(Violation(RuleId.LEVEL,
                                 f"{code} is a level {course.level} course; student is level {p.level}"))
        missing = [r for r in course.prerequisites if r not in passed]
        if missing:
            out.append(Violation(RuleId.PREREQ, f"missing prerequisite(s): {', '.join(missing)}"))
        have = self.passed_credits(p)
        if have < course.min_credits_passed:
            out.append(Violation(RuleId.MIN_CREDITS,
                                 f"requires {course.min_credits_passed} passed credit hours; student has {have}"))
        if course.min_gpa is not None:
            if p.gpa is None:
                out.append(Violation(RuleId.MIN_GPA, f"requires GPA >= {course.min_gpa}; student has no GPA yet"))
            elif p.gpa < course.min_gpa:
                out.append(Violation(RuleId.MIN_GPA,
                                     f"requires GPA >= {course.min_gpa}; student GPA is {p.gpa:.2f}"))
        if check_coreq:
            for co in course.corequisites:
                if co not in passed and self.violations(p, co, check_coreq=False):
                    reasons = "; ".join(v.message for v in self.violations(p, co, check_coreq=False))
                    out.append(Violation(RuleId.COREQ, f"corequisite {co} cannot be registered ({reasons})"))
        return out

    def is_eligible(self, p: StudentProfile, code: str) -> bool:
        return not self.violations(p, code)
