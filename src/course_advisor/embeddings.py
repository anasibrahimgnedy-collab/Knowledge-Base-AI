"""Embedding back-ends.

``TfidfEmbedder`` works offline with no model download and is the default.
``SentenceTransformerEmbedder`` uses a pretrained neural model when the
optional ``sentence-transformers`` package is installed.
"""
from __future__ import annotations

from typing import Protocol

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class Embedder(Protocol):
    name: str

    def fit(self, texts: list[str]) -> None: ...
    def embed(self, texts: list[str]) -> np.ndarray: ...


class TfidfEmbedder:
    """TF-IDF vectors (unigrams + bigrams), L2-normalised."""

    name = "tfidf"

    def __init__(self) -> None:
        self._vec = TfidfVectorizer(ngram_range=(1, 2), stop_words="english",
                                    sublinear_tf=True, norm="l2")
        self._fitted = False

    def fit(self, texts: list[str]) -> None:
        self._vec.fit(texts)
        self._fitted = True

    def embed(self, texts: list[str]) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("TfidfEmbedder.fit() must be called before embed()")
        return self._vec.transform(texts).toarray()


class SentenceTransformerEmbedder:
    """Pretrained transformer embeddings (optional dependency)."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - optional path
            raise ImportError("pip install sentence-transformers to use this embedder") from exc
        self.name = f"sbert:{model_name}"
        self._model = SentenceTransformer(model_name)

    def fit(self, texts: list[str]) -> None:  # no fitting required
        return None

    def embed(self, texts: list[str]) -> np.ndarray:  # pragma: no cover - optional path
        return np.asarray(self._model.encode(texts, normalize_embeddings=True))


def make_embedder(kind: str = "tfidf") -> Embedder:
    if kind == "tfidf":
        return TfidfEmbedder()
    if kind == "sbert":
        return SentenceTransformerEmbedder()
    raise ValueError(f"unknown embedder '{kind}' (expected 'tfidf' or 'sbert')")
