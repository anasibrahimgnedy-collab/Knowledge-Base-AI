"""Project-wide constants and default paths."""
from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KB_DIR = PROJECT_ROOT / "kb"
COURSES_DIR = KB_DIR / "courses"
POLICIES_DIR = KB_DIR / "policies"
PROFILES_DIR = PROJECT_ROOT / "profiles"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

# Chunking
CHUNK_MAX_WORDS = 120
CHUNK_OVERLAP_WORDS = 20

# Retrieval
DEFAULT_TOP_K = 3

# Ranking weights (documented in docs/REPORT.md)
WEIGHT_RELEVANCE = 1.0      # similarity between student interests and course text
WEIGHT_CORE = 0.45          # degree-required course
WEIGHT_AT_LEVEL = 0.15      # course level equals student level
WEIGHT_REQUESTED = 2.0      # student explicitly asked for the course

# Fallback academic terms
VALID_TERMS = ("Fall", "Spring")

# LLM
DEFAULT_LLM_MODEL = "claude-sonnet-5-5"
LLM_MAX_TOKENS = 700
