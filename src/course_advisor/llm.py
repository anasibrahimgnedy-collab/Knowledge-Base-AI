"""LLM access.  The LLM only phrases answers; it never decides eligibility."""
from __future__ import annotations

import logging
import os
from typing import Protocol

from . import config

log = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a college course-registration advisor chatbot. Answer ONLY from the FACTS block. "
    "The facts come from a deterministic rule engine and from retrieved official-style documents; "
    "never invent courses, prerequisites, credit hours or policies, and never recommend a course the "
    "facts do not list as accepted. Mention the source document for every claim. Be concise and friendly. "
    "These policies are fictional sample data; say so if asked about their origin."
)


class LLMClient(Protocol):
    name: str

    def complete(self, system: str, user: str) -> str: ...


class AnthropicLLM:
    """Pretrained LLM via the Anthropic API (requires ANTHROPIC_API_KEY)."""

    def __init__(self, model: str | None = None) -> None:
        import anthropic  # optional dependency
        self._client = anthropic.Anthropic()
        self.model = model or os.environ.get("ADVISOR_LLM_MODEL", config.DEFAULT_LLM_MODEL)
        self.name = f"anthropic:{self.model}"

    def complete(self, system: str, user: str) -> str:
        msg = self._client.messages.create(
            model=self.model, max_tokens=config.LLM_MAX_TOKENS, system=system,
            messages=[{"role": "user", "content": user}])
        return "".join(block.text for block in msg.content if getattr(block, "type", "") == "text")


def default_llm() -> LLMClient | None:
    """Return a live LLM if configured, else None (the chatbot then uses grounded templates)."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.info("ANTHROPIC_API_KEY not set: chatbot runs in offline template mode")
        return None
    try:
        return AnthropicLLM()
    except ImportError:
        log.warning("anthropic package not installed: chatbot runs in offline template mode")
        return None
