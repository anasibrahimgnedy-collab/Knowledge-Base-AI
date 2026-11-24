import pytest

from course_advisor.chatbot import AdvisorChat
from course_advisor.profiles import load_all_profiles


class FakeLLM:
    name = "fake"

    def __init__(self, answer=None, error=None):
        self.answer, self.error, self.prompts = answer, error, []

    def complete(self, system, user):
        self.prompts.append((system, user))
        if self.error:
            raise self.error
        return self.answer or "ok"


@pytest.fixture()
def profile():
    return load_all_profiles()[3]      # Youssef: unmet prerequisites


def test_show_plan_offline(advisor, profile):
    reply = AdvisorChat(advisor, profile).handle("Show my recommended plan")
    assert "Recommended plan" in reply.text and not reply.used_llm and reply.sources


def test_change_credit_load_updates_plan(advisor, profile):
    chat = AdvisorChat(advisor, profile)
    chat.handle("I want 12 credits")
    assert chat.plan.total_credits <= 12 and chat.profile.preferred_credits == 12
    assert profile.preferred_credits == 18, "original profile must not be mutated"


def test_add_interest_and_course_request(advisor, profile):
    chat = AdvisorChat(advisor, profile)
    assert "added interest" in chat.handle("I am interested in cybersecurity").text
    assert "cybersecurity" in chat.profile.interests
    chat.handle("I want to take CS206")
    assert "CS206" in chat.profile.requested_courses
    assert chat.plan.decisions["CS206"].verdict.value == "REJECTED"
    chat.handle("remove CS206")
    assert "CS206" not in chat.profile.requested_courses


def test_why_rejected_cites_rule_and_source(advisor, profile):
    reply = AdvisorChat(advisor, profile).handle("Why can't I take CS302?")
    assert "CS202" in reply.text and "NOT allowed" in reply.text
    assert any("prerequisite_policy" in s for s in reply.sources)


def test_why_recommended_and_unknown_course(advisor, profile):
    chat = AdvisorChat(advisor, profile)
    assert "recommended" in chat.handle("why CS301").text
    assert "could not find" in chat.handle("why ZZ999").text


def test_alternative_plans(advisor, profile):
    assert "alternative" in AdvisorChat(advisor, profile).handle("show me alternative plans").text.lower()


def test_free_question_answered_from_kb(advisor, profile):
    reply = AdvisorChat(advisor, profile).handle("What is the maximum number of credits on probation?")
    assert "credit_load_policy" in reply.text and reply.sources


def test_empty_message(advisor, profile):
    assert "Please type" in AdvisorChat(advisor, profile).handle("  ").text


def test_llm_receives_only_grounded_facts_and_may_rephrase(advisor, profile):
    llm = FakeLLM("You can register for CS301 and MATH202 next semester.")
    reply = AdvisorChat(advisor, profile, llm).handle("show my plan")
    assert reply.used_llm and "CS301" in reply.text
    system, user = llm.prompts[0]
    assert "FACTS" in user and "Answer ONLY from the FACTS" in system


def test_llm_hallucinated_course_falls_back_to_template(advisor, profile):
    llm = FakeLLM("Definitely take CS499 Quantum Basket Weaving!")
    reply = AdvisorChat(advisor, profile, llm).handle("show my plan")
    assert not reply.used_llm and "CS499" not in reply.text and "Recommended plan" in reply.text


def test_llm_failure_falls_back_to_template(advisor, profile):
    reply = AdvisorChat(advisor, profile, FakeLLM(error=RuntimeError("network down"))).handle("show my plan")
    assert not reply.used_llm and "Recommended plan" in reply.text


def test_default_llm_none_without_key(monkeypatch):
    from course_advisor.llm import default_llm
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    assert default_llm() is None


def test_alternatives_explains_when_only_one_plan_exists(advisor, monkeypatch):
    p = load_all_profiles()[0]
    chat = AdvisorChat(advisor, p)
    monkeypatch.setattr(advisor, "alternatives", lambda profile: [chat.plan])
    assert "No different plan exists" in chat.handle("show me other plan options").text
