"""Document parsing and chunking for the knowledge base.

Documents are Markdown with a ``key: value`` metadata block between the title
and the first ``##`` heading.  Every ``##`` section becomes one or more chunks.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

from . import config
from .models import Chunk, Course, CreditPolicy

log = logging.getLogger(__name__)


class KnowledgeBaseError(ValueError):
    """Raised when a knowledge-base document is malformed."""


@dataclass(frozen=True)
class Document:
    doc_id: str
    doc_type: str
    title: str
    source_file: str
    metadata: dict[str, str]
    sections: tuple[tuple[str, str], ...]   # (heading, body)


def parse_document(path: Path, doc_type: str) -> Document:
    """Parse one Markdown knowledge-base file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# "):
        raise KnowledgeBaseError(f"{path.name}: first line must be a '# Title' heading")
    title = lines[0][2:].strip()
    metadata: dict[str, str] = {}
    sections: list[tuple[str, list[str]]] = []
    for line in lines[1:]:
        if line.startswith("## "):
            sections.append((line[3:].strip(), []))
        elif sections:
            sections[-1][1].append(line)
        elif ":" in line and not line.startswith(">"):
            key, _, value = line.partition(":")
            metadata[key.strip()] = value.strip()
    parsed = tuple((h, " ".join(" ".join(b).split())) for h, b in sections)
    if not parsed:
        raise KnowledgeBaseError(f"{path.name}: no '##' sections found")
    doc_id = metadata.get("code") or metadata.get("doc_id") or path.stem
    return Document(doc_id, doc_type, title, path.name, metadata, parsed)


def load_documents(courses_dir: Path = config.COURSES_DIR,
                   policies_dir: Path = config.POLICIES_DIR) -> list[Document]:
    docs: list[Document] = []
    for directory, doc_type in ((courses_dir, "course"), (policies_dir, "policy")):
        files = sorted(directory.glob("*.md"))
        if not files:
            raise KnowledgeBaseError(f"no knowledge-base documents found in {directory}")
        docs.extend(parse_document(f, doc_type) for f in files)
    log.info("Parsed %d documents", len(docs))
    return docs


def split_words(text: str, max_words: int, overlap: int) -> list[str]:
    """Split text into windows of at most ``max_words`` words with overlap."""
    if overlap >= max_words:
        raise ValueError("overlap must be smaller than max_words")
    words = text.split()
    if len(words) <= max_words:
        return [text]
    step = max_words - overlap
    pieces = []
    for start in range(0, len(words), step):
        pieces.append(" ".join(words[start:start + max_words]))
        if start + max_words >= len(words):
            break
    return pieces


def chunk_documents(docs: list[Document],
                    max_words: int = config.CHUNK_MAX_WORDS,
                    overlap: int = config.CHUNK_OVERLAP_WORDS) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in docs:
        context = f"{doc.title}. {doc.metadata.get('tags', '')}".strip()
        for s_idx, (heading, body) in enumerate(doc.sections):
            for p_idx, piece in enumerate(split_words(body, max_words, overlap)):
                chunks.append(Chunk(
                    chunk_id=f"{doc.doc_id}#{s_idx}.{p_idx}",
                    doc_id=doc.doc_id,
                    doc_type=doc.doc_type,
                    source_file=f"kb/{'courses' if doc.doc_type == 'course' else 'policies'}/{doc.source_file}",
                    section=heading,
                    text=piece,
                    retrieval_text=f"{context}. {heading}. {piece}",
                ))
    return chunks


def _split_list(value: str) -> tuple[str, ...]:
    return () if value.strip().lower() in ("", "none") else tuple(
        v.strip() for v in value.split(",") if v.strip())


def _require(doc: Document, key: str) -> str:
    if key not in doc.metadata:
        raise KnowledgeBaseError(f"{doc.source_file}: missing required field '{key}'")
    return doc.metadata[key]


def build_course(doc: Document) -> Course:
    try:
        gpa_raw = _require(doc, "min_gpa")
        course = Course(
            code=_require(doc, "code"),
            title=_require(doc, "title"),
            credits=int(_require(doc, "credits")),
            level=int(_require(doc, "level")),
            offered=_split_list(_require(doc, "offered")),
            prerequisites=_split_list(_require(doc, "prerequisites")),
            corequisites=_split_list(_require(doc, "corequisites")),
            min_credits_passed=int(_require(doc, "min_credits_passed")),
            min_gpa=None if gpa_raw.lower() == "none" else float(gpa_raw),
            category=_require(doc, "category"),
            tags=_split_list(doc.metadata.get("tags", "")),
            source_file=f"kb/courses/{doc.source_file}",
        )
    except ValueError as exc:
        raise KnowledgeBaseError(f"{doc.source_file}: invalid field value ({exc})") from exc
    if not set(course.offered) <= set(config.VALID_TERMS):
        raise KnowledgeBaseError(f"{doc.source_file}: offered must be Fall and/or Spring")
    return course


def build_courses(docs: list[Document]) -> dict[str, Course]:
    courses: dict[str, Course] = {}
    for doc in docs:
        if doc.doc_type != "course":
            continue
        course = build_course(doc)
        if course.code in courses:
            raise KnowledgeBaseError(f"duplicate course code {course.code}")
        courses[course.code] = course
    for course in courses.values():
        for ref in (*course.prerequisites, *course.corequisites):
            if ref not in courses:
                raise KnowledgeBaseError(f"{course.code} references unknown course {ref}")
    return courses


def build_credit_policy(docs: list[Document]) -> CreditPolicy:
    doc = next((d for d in docs if d.doc_id == "POL-CREDIT"), None)
    if doc is None:
        raise KnowledgeBaseError("credit load policy (POL-CREDIT) not found")
    try:
        m = doc.metadata
        return CreditPolicy(
            min_full_time=int(m["min_credits_full_time"]),
            max_probation=int(m["max_credits_probation"]),
            max_standard=int(m["max_credits_standard"]),
            max_honors=int(m["max_credits_honors"]),
            max_first_semester=int(m["max_credits_first_semester"]),
            gpa_probation_below=float(m["gpa_probation_below"]),
            gpa_honors_from=float(m["gpa_honors_from"]),
        )
    except (KeyError, ValueError) as exc:
        raise KnowledgeBaseError(f"POL-CREDIT: invalid or missing parameter ({exc})") from exc
