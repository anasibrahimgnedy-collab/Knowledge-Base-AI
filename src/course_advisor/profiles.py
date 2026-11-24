"""Load student profiles from JSON files."""
from __future__ import annotations

import json
from pathlib import Path

from . import config
from .models import StudentProfile

_FIELDS = {"name", "level", "term", "passed_courses", "gpa", "skills", "interests", "goals",
           "preferred_credits", "requested_courses", "description"}


def profile_from_dict(data: dict) -> StudentProfile:
    unknown = set(data) - _FIELDS
    if unknown:
        raise ValueError(f"unknown profile fields: {sorted(unknown)}")
    for key in ("name", "level", "term"):
        if key not in data:
            raise ValueError(f"profile is missing required field '{key}'")
    return StudentProfile(**data)


def load_profile(path: Path) -> StudentProfile:
    try:
        return profile_from_dict(json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path.name}: invalid JSON ({exc})") from exc


def load_all_profiles(directory: Path = config.PROFILES_DIR) -> list[StudentProfile]:
    files = sorted(directory.glob("profile_*.json"))
    if not files:
        raise FileNotFoundError(f"no profile_*.json files in {directory}")
    return [load_profile(f) for f in files]
