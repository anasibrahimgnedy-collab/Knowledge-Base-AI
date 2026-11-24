import pytest

from course_advisor import config
from course_advisor.knowledge_base import (
    KnowledgeBaseError,
    build_courses,
    build_credit_policy,
    chunk_documents,
    load_documents,
    parse_document,
    split_words,
)


@pytest.fixture(scope="module")
def docs():
    return load_documents()


def test_all_documents_parse_and_counts(docs):
    assert sum(d.doc_type == "course" for d in docs) == 30
    assert sum(d.doc_type == "policy" for d in docs) == 4


def test_every_document_is_labelled_fictional():
    for path in [*config.COURSES_DIR.glob("*.md"), *config.POLICIES_DIR.glob("*.md")]:
        assert "FICTIONAL" in path.read_text(), path.name


def test_courses_have_no_dangling_references(docs):
    courses = build_courses(docs)
    for c in courses.values():
        assert set(c.prerequisites) | set(c.corequisites) <= set(courses)
        assert c.credits > 0 and 1 <= c.level <= 4


def test_prerequisites_never_point_to_same_or_higher_level_course(docs):
    courses = build_courses(docs)
    for c in courses.values():
        for pre in c.prerequisites:
            assert courses[pre].level <= c.level


def test_no_prerequisite_cycles(docs):
    courses = build_courses(docs)

    def visit(code, stack):
        assert code not in stack, f"cycle through {code}"
        for pre in courses[code].prerequisites:
            visit(pre, stack | {code})
    for code in courses:
        visit(code, frozenset())


def test_credit_policy_numbers_match_policy_prose(docs):
    pol = build_credit_policy(docs)
    prose = " ".join(" ".join(b for _, b in d.sections) for d in docs if d.doc_id == "POL-CREDIT")
    for n in (pol.max_probation, pol.max_standard, pol.max_honors, pol.min_full_time):
        assert str(n) in prose
    assert str(pol.gpa_probation_below) in prose and str(pol.gpa_honors_from) in prose


def test_course_overview_text_matches_structured_fields(docs):
    """Evidence text and rule-engine data come from one file and must agree."""
    courses = build_courses(docs)
    for d in docs:
        if d.doc_type != "course":
            continue
        overview = dict(d.sections)["Overview"]
        c = courses[d.doc_id]
        assert f"{c.credits}-credit-hour" in overview
        for pre in c.prerequisites:
            assert pre in overview


def test_chunks_cover_every_section_and_carry_sources(docs):
    chunks = chunk_documents(docs)
    assert all(c.source_file.startswith("kb/") for c in chunks)
    assert len({c.chunk_id for c in chunks}) == len(chunks)
    assert {c.section for c in chunks if c.doc_id == "CS101"} == {"Overview", "Description", "Topics",
                                                                   "Registration notes"}


def test_split_words_overlap_and_validation():
    text = " ".join(f"w{i}" for i in range(250))
    pieces = split_words(text, 100, 20)
    assert len(pieces) == 3 and pieces[0].split()[-20:] == pieces[1].split()[:20]
    assert " ".join(pieces[-1].split()[-1:]) == "w249"
    assert split_words("short text", 100, 20) == ["short text"]
    with pytest.raises(ValueError):
        split_words(text, 10, 10)


def test_malformed_documents_raise(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text("no heading here\n")
    with pytest.raises(KnowledgeBaseError):
        parse_document(bad, "course")
    nosec = tmp_path / "nosec.md"
    nosec.write_text("# Title\ncode: X1\n")
    with pytest.raises(KnowledgeBaseError):
        parse_document(nosec, "course")


def test_invalid_course_field_raises(tmp_path):
    f = tmp_path / "X.md"
    f.write_text("# X\ncode: X100\ntitle: X\ncredits: three\nlevel: 1\noffered: Fall\nprerequisites: none\n"
                 "corequisites: none\nmin_credits_passed: 0\nmin_gpa: none\ncategory: core\n## Overview\ntext\n")
    with pytest.raises(KnowledgeBaseError):
        build_courses([parse_document(f, "course")])
