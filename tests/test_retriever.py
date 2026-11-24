import pytest

from course_advisor.embeddings import make_embedder


def test_ml_query_finds_machine_learning_course(advisor):
    hits = advisor.retriever.retrieve("machine learning and neural networks", 5, doc_type="course")
    assert "CS304" in {h.chunk.doc_id for h in hits[:3]}


def test_credit_query_finds_credit_policy(advisor):
    hit = advisor.retriever.retrieve("maximum credit hours for a student with GPA below 2.0", 1)[0]
    assert hit.chunk.doc_id == "POL-CREDIT"


def test_filters_and_empty_query(advisor):
    r = advisor.retriever
    assert r.retrieve("   ") == []
    assert all(h.chunk.doc_type == "policy" for h in r.retrieve("prerequisite", 5, doc_type="policy"))
    assert all(h.chunk.doc_id == "CS201" for h in r.retrieve("trees", 3, doc_id="CS201"))
    assert all(h.chunk.section == "Overview" for h in r.retrieve("offered", 3, section="Overview"))


def test_scores_sorted_descending(advisor):
    hits = advisor.retriever.retrieve("database sql", 5)
    assert [h.score for h in hits] == sorted((h.score for h in hits), reverse=True)


def test_course_relevance_scaled(advisor):
    rel = advisor.retriever.course_relevance("cybersecurity cryptography")
    assert max(rel.values()) == pytest.approx(1.0) and min(rel.values()) >= 0
    assert max(rel, key=rel.get) in {"CS305", "CS405"}
    assert advisor.retriever.course_relevance("") == {}


def test_embedder_factory_and_unfitted_error():
    with pytest.raises(ValueError):
        make_embedder("nope")
    with pytest.raises(RuntimeError):
        make_embedder("tfidf").embed(["x"])
