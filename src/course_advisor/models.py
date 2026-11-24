"""Plain data structures shared across the system."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


@dataclass(frozen=True)
class Chunk:
    """A retrievable passage of a knowledge-base document."""

    chunk_id: str
    doc_id: str
    doc_type: str          # "course" | "policy"
    source_file: str
    section: str
    text: str              # text shown as evidence
    retrieval_text: str    # text that is embedded (adds title/tags context)


@dataclass(frozen=True)
class Hit:
    """A chunk returned by the retriever with its similarity score."""

    chunk: Chunk
    score: float


@dataclass(frozen=True)
class Course:
    code: str
    title: str
    credits: int
    level: int
    offered: tuple[str, ...]
    prerequisites: tuple[str, ...]
    corequisites: tuple[str, ...]
    min_credits_passed: int
    min_gpa: float | None
    category: str
    tags: tuple[str, ...]
    source_file: str


@dataclass(frozen=True)
class CreditPolicy:
    """Numeric parameters read from the credit-load policy document."""

    min_full_time: int
    max_probation: int
    max_standard: int
    max_honors: int
    max_first_semester: int
    gpa_probation_below: float
    gpa_honors_from: float


@dataclass
class StudentProfile:
    name: str
    level: int
    term: str                                   # "Fall" | "Spring"
    passed_courses: list[str] = field(default_factory=list)
    gpa: float | None = None                    # None = no GPA yet (first semester)
    skills: list[str] = field(default_factory=list)
    interests: list[str] = field(default_factory=list)
    goals: str = ""
    preferred_credits: int = 15
    requested_courses: list[str] = field(default_factory=list)
    description: str = ""                       # scenario label for the test report

    def interest_query(self) -> str:
        parts = [*self.interests, *self.interests, self.goals, *self.skills]
        return " ".join(p for p in parts if p).strip()


class Verdict(str, Enum):
    RECOMMENDED = "RECOMMENDED"
    ELIGIBLE_NOT_SELECTED = "ELIGIBLE_NOT_SELECTED"
    REJECTED = "REJECTED"
    ALREADY_PASSED = "ALREADY_PASSED"


class RuleId(str, Enum):
    ALREADY_PASSED = "ALREADY_PASSED"
    NOT_OFFERED = "NOT_OFFERED_THIS_TERM"
    LEVEL = "LEVEL_RESTRICTION"
    PREREQ = "PREREQUISITE_UNMET"
    MIN_CREDITS = "MIN_PASSED_CREDITS"
    MIN_GPA = "MIN_GPA"
    COREQ = "COREQUISITE_UNAVAILABLE"
    CREDIT_LIMIT = "CREDIT_LIMIT_EXCEEDED"
    UNKNOWN_COURSE = "UNKNOWN_COURSE"


@dataclass(frozen=True)
class Violation:
    rule: RuleId
    message: str


@dataclass
class Decision:
    course_code: str
    verdict: Verdict
    violations: list[Violation] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)   # why recommended / not selected
    score: float = 0.0
    relevance: float = 0.0
    evidence: list[Hit] = field(default_factory=list)          # course-document passages
    policy_evidence: list[Hit] = field(default_factory=list)   # policy passages for each failed rule


@dataclass
class Plan:
    profile: StudentProfile
    max_credits: int
    target_credits: int
    selected: list[str]
    total_credits: int
    decisions: dict[str, Decision]
    warnings: list[str] = field(default_factory=list)
    policy_evidence: dict[str, list[Hit]] = field(default_factory=dict)
    label: str = "primary"

    def by_verdict(self, verdict: Verdict) -> list[Decision]:
        items = [d for d in self.decisions.values() if d.verdict is verdict]
        return sorted(items, key=lambda d: (-d.score, d.course_code))
