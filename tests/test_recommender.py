import random

import pytest

from course_advisor.models import RuleId, StudentProfile, Verdict
from course_advisor.profiles import load_all_profiles


def assert_plan_valid(advisor, plan):
    """Independent invariants every plan must satisfy, regardless of ranking."""
    p, rules = plan.profile, advisor.rules
    assert plan.total_credits == sum(advisor.courses[c].credits for c in plan.selected)
    assert plan.total_credits <= plan.max_credits, "credit limit violated"
    assert len(set(plan.selected)) == len(plan.selected)
    for code in plan.selected:
        assert code not in p.passed_courses
        assert not rules.violations(p, code), f"{code} recommended but ineligible"
        course = advisor.courses[code]
        for co in course.corequisites:
            assert co in p.passed_courses or co in plan.selected, f"{code} missing corequisite {co}"
        assert plan.decisions[code].evidence, f"{code} has no retrieved evidence"
        assert plan.decisions[code].reasons
    for code, d in plan.decisions.items():
        if d.verdict is Verdict.REJECTED:
            assert d.violations, f"{code} rejected with no stated reason"
            assert code not in plan.selected


@pytest.mark.parametrize("profile", load_all_profiles(), ids=lambda p: p.name)
def test_every_profile_plan_is_valid(advisor, profile):
    assert_plan_valid(advisor, advisor.plan(profile))


def test_unmet_prerequisite_is_rejected_with_reason_and_hint(advisor):
    p = StudentProfile("U", 3, "Spring", ["CS101", "CS102", "CS201", "MATH101", "MATH102", "CS103"],
                       3.0, interests=["operating systems"], requested_courses=["CS302"])
    plan = advisor.plan(p)
    d = plan.decisions["CS302"]
    assert d.verdict is Verdict.REJECTED
    assert any(v.rule is RuleId.PREREQ and "CS202" in v.message for v in d.violations)
    assert any("CS202" in h for h in d.reasons)
    assert d.policy_evidence and "prerequisite" in d.policy_evidence[0].chunk.source_file


def test_credit_limit_enforced_and_overflow_rejected(advisor):
    p = StudentProfile("C", 3, "Spring", ["CS101", "MATH101", "ENG101", "HUM101", "CS103", "CS102", "MATH102",
                                          "CS201", "MATH201", "MATH202", "CS205", "CS202", "CS203"],
                       2.4, preferred_credits=24,
                       requested_courses=["CS301", "CS302", "CS303", "CS303L", "CS304", "CS305", "CS307", "CS204"])
    plan = advisor.plan(p)
    assert plan.max_credits == 18 and plan.total_credits <= 18
    assert any("exceeds the maximum" in w for w in plan.warnings)
    over = [c for c, d in plan.decisions.items()
            if any(v.rule is RuleId.CREDIT_LIMIT for v in d.violations)]
    assert over, "some requested courses must be rejected for exceeding the limit"
    assert plan.policy_evidence["CREDIT_LIMIT_EXCEEDED"][0].chunk.doc_id == "POL-CREDIT"


def test_probation_student_capped_at_12(advisor):
    p = StudentProfile("P", 2, "Spring", ["CS101", "MATH101", "CS103", "ENG101", "HUM101", "CS102", "MATH102"],
                       1.5, preferred_credits=18)
    plan = advisor.plan(p)
    assert plan.max_credits == 12 and plan.total_credits <= 12


def test_corequisite_bundled_with_course(advisor):
    p = StudentProfile("B", 3, "Spring", ["CS101", "CS102", "CS103", "CS202"], 3.0,
                       requested_courses=["CS303L"], preferred_credits=12)
    plan = advisor.plan(p)
    assert "CS303L" in plan.selected and "CS303" in plan.selected
    assert "Corequisite" in plan.decisions["CS303"].reasons[0]


def test_requested_course_prioritised(advisor):
    base = dict(name="R", level=2, term="Spring", gpa=3.0,
                passed_courses=["CS101", "MATH101", "CS103", "ENG101", "HUM101", "CS102", "MATH102"],
                preferred_credits=3)
    plan = advisor.plan(StudentProfile(requested_courses=["CS204"], **base))
    assert plan.selected == ["CS204"]


def test_first_semester_student_gets_first_semester_limit(advisor):
    plan = advisor.plan(StudentProfile("N", 1, "Fall", [], None, preferred_credits=21))
    assert plan.max_credits == 18 and plan.total_credits <= 18


def test_passed_course_never_recommended(advisor):
    p = StudentProfile("D", 1, "Spring", ["CS101"], 3.0, requested_courses=["CS101"])
    plan = advisor.plan(p)
    assert plan.decisions["CS101"].verdict is Verdict.ALREADY_PASSED and "CS101" not in plan.selected


def test_unknown_requested_course_rejected(advisor):
    plan = advisor.plan(StudentProfile("X", 1, "Spring", [], None, requested_courses=["ZZ999"]))
    assert plan.decisions["ZZ999"].verdict is Verdict.REJECTED


def test_interest_changes_ranking(advisor):
    base = dict(name="I", level=3, term="Spring", gpa=3.5, preferred_credits=6,
                passed_courses=["CS101", "MATH101", "ENG101", "HUM101", "CS103", "CS102", "MATH102", "CS201",
                                "MATH201", "MATH202", "CS205", "CS202", "CS203", "CS204"])
    ml = advisor.plan(StudentProfile(interests=["machine learning"], **base), preset="interest_first")
    sec = advisor.plan(StudentProfile(interests=["cybersecurity cryptography"], **base), preset="interest_first")
    assert "CS304" in ml.selected and "CS305" in sec.selected


def test_alternatives_are_distinct_and_valid(advisor):
    profile = load_all_profiles()[5]
    plans = advisor.alternatives(profile)
    assert len(plans) >= 2
    assert len({tuple(sorted(p.selected)) for p in plans}) == len(plans)
    for plan in plans:
        assert_plan_valid(advisor, plan)


def test_low_load_warning(advisor):
    plan = advisor.plan(StudentProfile("W", 1, "Spring", [], None))
    assert plan.total_credits >= 12 or any("full-time" in w for w in plan.warnings)


def test_fuzz_random_profiles_never_violate_rules(advisor):
    """Seeded fuzz: random histories/requests must never yield an ineligible or over-limit plan."""
    rng = random.Random(2026)
    codes = sorted(advisor.courses)
    for i in range(150):
        passed = rng.sample(codes, rng.randint(0, 20))
        profile = StudentProfile(
            name=f"fuzz{i}", level=rng.randint(1, 4), term=rng.choice(["Fall", "Spring"]),
            passed_courses=passed, gpa=rng.choice([None, 1.2, 2.0, 2.7, 3.0, 3.9]),
            interests=rng.sample(["machine learning", "security", "web", "databases", "cloud", "ethics"], 2),
            preferred_credits=rng.randint(3, 24), requested_courses=rng.sample(codes, rng.randint(0, 8)))
        assert_plan_valid(advisor, advisor.plan(profile))


def test_packing_reaches_best_achievable_load(advisor):
    """Greedy would stop at 10 credit hours here; the exact packer finds 12 (four 3-credit courses)."""
    karim = next(p for p in load_all_profiles() if p.name == "Karim Samir")
    plan = advisor.plan(karim)
    assert plan.total_credits == 12 and not any("full-time" in w for w in plan.warnings)


def test_requested_overflow_message_is_accurate(advisor):
    p = StudentProfile("O", 3, "Spring", ["CS101", "MATH101", "ENG101", "HUM101", "CS103", "CS102", "MATH102",
                                          "CS201", "MATH201", "MATH202", "CS205", "CS202", "CS203"],
                       2.4, preferred_credits=18,
                       requested_courses=["CS301", "CS302", "CS303", "CS305", "CS307", "CS304", "CS204"])
    plan = advisor.plan(p)
    overflow = [v for d in plan.decisions.values() for v in d.violations if v.rule is RuleId.CREDIT_LIMIT]
    assert overflow
    assert all("above the maximum of 18" in v.message for v in overflow)
    assert plan.total_credits == 18       # six 3-credit requested courses fit exactly
