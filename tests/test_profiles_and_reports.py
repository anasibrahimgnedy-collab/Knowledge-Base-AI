import json

import pytest

from course_advisor import cli
from course_advisor.models import RuleId, Verdict
from course_advisor.profiles import load_all_profiles, profile_from_dict
from course_advisor.report import plan_dict, plan_markdown


@pytest.fixture(scope="module")
def plans(advisor):
    return {p.name: advisor.plan(p) for p in load_all_profiles()}


def test_at_least_six_profiles_with_different_levels():
    profiles = load_all_profiles()
    assert len(profiles) >= 6
    assert {p.level for p in profiles} == {1, 2, 3, 4}


def test_profile_histories_are_internally_consistent(advisor):
    """A student's passed courses must themselves satisfy prerequisites (realistic synthetic data)."""
    for p in load_all_profiles():
        for code in p.passed_courses:
            assert set(advisor.courses[code].prerequisites) <= set(p.passed_courses), (p.name, code)
            assert advisor.courses[code].level <= p.level


def test_required_scenarios_present(plans):
    all_rules = {name: {v.rule for d in pl.decisions.values() for v in d.violations} for name, pl in plans.items()}
    assert any(RuleId.PREREQ in r for r in all_rules.values()), "no unmet-prerequisite test case"
    assert any(RuleId.CREDIT_LIMIT in r for r in all_rules.values()), "no credit-limit test case"


def test_specific_expected_outcomes(plans):
    assert "CS103" not in plans["Amira Hassan"].selected                    # Fall-only
    assert plans["Omar Khaled"].decisions["CS204"].verdict is Verdict.REJECTED   # level
    assert plans["Youssef Adel"].decisions["CS302"].verdict is Verdict.REJECTED  # prerequisite
    assert plans["Sara Nabil"].total_credits <= 18
    assert "CS401" in plans["Nour Fathy"].selected                          # eligible capstone
    assert plans["Nour Fathy"].decisions["CS404"].verdict is Verdict.REJECTED    # Fall-only
    karim = plans["Karim Samir"]
    assert karim.max_credits == 12 and "CS401" not in karim.selected
    assert {v.rule for v in karim.decisions["CS401"].violations} >= {RuleId.MIN_CREDITS, RuleId.MIN_GPA}
    assert karim.decisions["CS101"].verdict is Verdict.ALREADY_PASSED


def test_markdown_report_has_all_required_sections(advisor, plans):
    md = plan_markdown(plans["Sara Nabil"], advisor.courses)
    for heading in ("## 1. Student input", "## 2. Retrieved evidence", "## 3. Accepted courses",
                    "## 4. Rejected courses and reasons", "## 5. Final recommendation"):
        assert heading in md
    assert "kb/policies/credit_load_policy.md" in md and "kb/courses/CS301.md" in md


def test_json_report_roundtrips(plans):
    data = json.loads(json.dumps(plan_dict(plans["Youssef Adel"])))
    assert data["decisions"]["CS302"]["verdict"] == "REJECTED"
    assert data["decisions"]["CS302"]["evidence"]


def test_cli_run_profiles_writes_outputs(tmp_path):
    written = cli.run_profiles(tmp_path)
    assert len(written) == 2 * len(load_all_profiles())
    assert all(f.stat().st_size > 0 for f in written)


def test_profile_loader_validation(tmp_path):
    with pytest.raises(ValueError):
        profile_from_dict({"name": "x", "level": 1, "term": "Fall", "bogus": 1})
    with pytest.raises(ValueError):
        profile_from_dict({"name": "x"})
    from course_advisor.profiles import load_profile
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    with pytest.raises(ValueError):
        load_profile(bad)
    with pytest.raises(FileNotFoundError):
        from course_advisor.profiles import load_all_profiles as la
        la(tmp_path / "missing")
