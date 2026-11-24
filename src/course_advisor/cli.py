"""Command line interface: ``python -m course_advisor {run-profiles,chat}``."""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from . import config
from .chatbot import AdvisorChat
from .llm import default_llm
from .profiles import load_all_profiles, load_profile
from .recommender import Advisor
from .report import plan_dict, plan_markdown


def run_profiles(out_dir: Path) -> list[Path]:
    advisor = Advisor.from_knowledge_base()
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for i, profile in enumerate(load_all_profiles(), 1):
        plan = advisor.plan(profile)
        md = out_dir / f"profile_{i:02d}.md"
        md.write_text(plan_markdown(plan, advisor.courses), encoding="utf-8")
        js = out_dir / f"profile_{i:02d}.json"
        js.write_text(json.dumps(plan_dict(plan), indent=2), encoding="utf-8")
        written += [md, js]
        print(f"{profile.name}: {plan.selected} ({plan.total_credits}/{plan.max_credits} cr)")
    return written


def chat(profile_path: Path) -> None:
    advisor = Advisor.from_knowledge_base()
    session = AdvisorChat(advisor, load_profile(profile_path), default_llm())
    print("Course Advisor (type 'quit' to exit). Try: 'show my plan', 'why CS301?', 'I want 12 credits'.")
    while True:
        try:
            msg = input("you> ")
        except EOFError:
            break
        if msg.strip().lower() in {"quit", "exit"}:
            break
        reply = session.handle(msg)
        print(f"advisor> {reply.text}")
        if reply.sources:
            print("sources:", "; ".join(reply.sources))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="course_advisor", description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    runp = sub.add_parser("run-profiles", help="run all test profiles and write outputs/")
    runp.add_argument("--out", type=Path, default=config.OUTPUTS_DIR)
    chatp = sub.add_parser("chat", help="interactive chatbot for one profile")
    chatp.add_argument("profile", type=Path)
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    if args.cmd == "run-profiles":
        run_profiles(args.out)
    else:
        chat(args.profile)
    return 0
