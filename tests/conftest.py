import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from course_advisor.recommender import Advisor  # noqa: E402


@pytest.fixture(scope="session")
def advisor() -> Advisor:
    return Advisor.from_knowledge_base()


@pytest.fixture(scope="session")
def rules(advisor):
    return advisor.rules
