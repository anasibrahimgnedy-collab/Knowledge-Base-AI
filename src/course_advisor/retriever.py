"""Vector retriever over knowledge-base chunks (cosine similarity)."""
from __future__ import annotations

import numpy as np

from . import config
from .embeddings import Embedder, make_embedder
from .models import Chunk, Hit


class Retriever:
    def __init__(self, chunks: list[Chunk], embedder: Embedder | None = None) -> None:
        if not chunks:
            raise ValueError("Retriever needs at least one chunk")
        self.chunks = chunks
        self.embedder = embedder or make_embedder("tfidf")
        texts = [c.retrieval_text for c in chunks]
        self.embedder.fit(texts)
        self.matrix = self.embedder.embed(texts)

    def retrieve(self, query: str, k: int = config.DEFAULT_TOP_K, *,
                 doc_type: str | None = None, doc_id: str | None = None,
                 section: str | None = None) -> list[Hit]:
        """Return the top-k chunks for ``query`` filtered by document type / id."""
        if not query.strip():
            return []
        q = self.embedder.embed([query])[0]
        scores = self.matrix @ q
        order = np.argsort(-scores, kind="stable")
        hits: list[Hit] = []
        for idx in order:
            chunk = self.chunks[int(idx)]
            if doc_type and chunk.doc_type != doc_type:
                continue
            if doc_id and chunk.doc_id != doc_id:
                continue
            if section and chunk.section != section:
                continue
            if scores[idx] <= 0:
                break
            hits.append(Hit(chunk, float(scores[idx])))
            if len(hits) == k:
                break
        return hits

    def course_relevance(self, query: str) -> dict[str, float]:
        """Best chunk similarity per course, min-max scaled to [0, 1]."""
        if not query.strip():
            return {}
        q = self.embedder.embed([query])[0]
        scores = self.matrix @ q
        best: dict[str, float] = {}
        for chunk, s in zip(self.chunks, scores, strict=True):
            if chunk.doc_type == "course":
                best[chunk.doc_id] = max(best.get(chunk.doc_id, 0.0), float(s))
        top = max(best.values(), default=0.0)
        return {k: v / top for k, v in best.items()} if top > 0 else {k: 0.0 for k in best}
