import pytest

from course_advisor.models import RuleId, StudentProfile
from course_advisor.rules import ProfileError


def prof(**kw):
    base = dict(name="T", level=3, term="Spring", passed_courses=[], gpa=3.0)
    base.update(kw)
    return StudentProfile(**base)


def rule_ids(rules, p, code):
    return {v.rule for v in rules.violations(p, code)}


@pytest.mark.parametrize("gpa,expected", [(None, 18), (0.0, 12), (1.99, 12), (2.0, 18), (2.99, 18),
                                          (3.0, 21), (4.0, 21)])
def test_credit_limit_boundaries(rules, gpa, expected):
    assert rules.max_credits(prof(gpa=gpa))[0] == expected


def test_prerequisite_unmet_and_met(rules):
    assert RuleId.PREREQ in rule_ids(rules, prof(passed_courses=["CS101"]), "CS201")
    assert rule_ids(rules, prof(level=2, passed_courses=["CS101", "CS102"]), "CS201") == set()


def test_all_prerequisites_required_not_any(rules):
    p = prof(passed_courses=["CS201"])           # CS301 needs CS201 AND MATH102
    v = rules.violations(p, "CS301")
    assert any("MATH102" in x.message for x in v)


def test_already_passed(rules):
    assert rule_ids(rules, prof(passed_courses=["CS101"]), "CS101") == {RuleId.ALREADY_PASSED}


def test_not_offered_this_term(rules):
    assert RuleId.NOT_OFFERED in rule_ids(rules, prof(term="Spring"), "CS206")
    assert RuleId.NOT_OFFERED not in rule_ids(rules, prof(term="Fall"), "CS206")


def test_level_restriction(rules):
    assert RuleId.LEVEL in rule_ids(rules, prof(level=1), "CS204")
    assert RuleId.LEVEL not in rule_ids(rules, prof(level=2), "CS204")


def test_min_passed_credits(rules):
    p = prof(level=4, passed_courses=["CS101", "CS205", "CS301", "CS102", "CS201", "MATH102"])
    assert RuleId.MIN_CREDITS in rule_ids(rules, p, "CS401")
    assert rules.passed_credits(p) == 4 + 3 + 3 + 3 + 4 + 3


def test_min_gpa_including_missing_gpa(rules):
    base = dict(level=4, passed_courses=["CS101", "MATH101", "CS304", "CS201", "MATH201", "MATH202"])
    assert RuleId.MIN_GPA in rule_ids(rules, prof(gpa=2.4, **base), "CS402")
    assert RuleId.MIN_GPA in rule_ids(rules, prof(gpa=None, **base), "CS402")
    assert RuleId.MIN_GPA not in rule_ids(rules, prof(gpa=2.5, **base), "CS402")


def test_corequisite_unavailable_when_coreq_ineligible(rules):
    assert RuleId.COREQ in rule_ids(rules, prof(passed_courses=[]), "CS303L")
    ok = prof(passed_courses=["CS101", "CS102", "CS103", "CS202"])
    assert rule_ids(rules, ok, "CS303L") == set()


def test_corequisite_satisfied_when_passed(rules):
    p = prof(passed_courses=["CS303"])
    assert rule_ids(rules, p, "CS303L") == set()


def test_unknown_course(rules):
    assert rule_ids(rules, prof(), "ZZ999") == {RuleId.UNKNOWN_COURSE}


@pytest.mark.parametrize("kw", [dict(level=5), dict(term="Summer"), dict(gpa=4.5), dict(gpa=-1.0),
                                dict(passed_courses=["NOPE1"])])
def test_invalid_profiles_rejected(rules, kw):
    with pytest.raises(ProfileError):
        rules.validate_profile(prof(**kw))


def test_invalid_preferred_credits(rules):
    with pytest.raises(ProfileError):
        rules.validate_profile(prof(preferred_credits=0))
