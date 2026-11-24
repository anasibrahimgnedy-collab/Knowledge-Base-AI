# Requirement Traceability Matrix

Status values: VERIFIED = evidence exists (test or executed output); BLOCKED = needs something outside this build.

| ID | Implementation | Evidence | Status |
|---|---|---|---|
| R-01 | `kb/courses/*.md` (30), `kb/policies/*.md` (4) | `test_knowledge_base.py` (counts, references, cycles, overview text agrees with fields) | VERIFIED |
| R-02 | Fictional banner in every KB file | `test_every_document_is_labelled_fictional` | VERIFIED |
| R-03 | `models.StudentProfile`, `profiles.py`, `profiles/*.json` | `test_profile_loader_validation`, `test_invalid_profiles_rejected` | VERIFIED |
| R-04 | `knowledge_base.py`, `embeddings.py`, `retriever.py`, `recommender.py` | `test_retriever.py`, `test_chunks_cover_every_section...`, notebook §1-2 | VERIFIED |
| R-05 | `rules.py` | `test_rules.py` (each rule, GPA boundaries, coreq, invalid profiles) | VERIFIED |
| R-06 | `recommender.py`, `report.py` | `test_recommender.py`, `outputs/profile_*.md` | VERIFIED |
| R-07 | `chatbot.py`, `llm.py` (Anthropic API + offline) | `test_chatbot.py` with fake LLMs; offline mode run in notebook §5. **Live API call not exercised** (no key) | VERIFIED for offline + guard logic; live API path BLOCKED (needs `ANTHROPIC_API_KEY`) |
| R-08 | `profiles/` has 7 profiles, levels 1-4 | `test_at_least_six_profiles_with_different_levels` | VERIFIED |
| R-09 | Profile 4 (Youssef) | `test_unmet_prerequisite_is_rejected_with_reason_and_hint`, `test_required_scenarios_present` | VERIFIED |
| R-10 | Profile 5 (Sara) | `test_credit_limit_enforced_and_overflow_rejected`, `test_required_scenarios_present` | VERIFIED |
| R-11 | `report.plan_markdown` sections 1-5 | `test_markdown_report_has_all_required_sections`; `outputs/`; notebook §4 | VERIFIED |
| R-12 | `notebooks/KBA_Course_Advisor.ipynb` (imports `src/course_advisor`) | Executed with 0 error outputs (`scripts/build_notebook.py`) | VERIFIED |
| R-13 | `kb/` | as R-01 | VERIFIED |
| R-14 | `requirements.txt`, `pyproject.toml` | Fresh-clone install of core deps + test run (see `final-verification.md`) | VERIFIED |
| R-15 | `README.md` | Commands executed from a fresh clone | VERIFIED |
| R-16 | `profiles/*.json` + `outputs/profile_*.{md,json}` | `test_cli_run_profiles_writes_outputs` | VERIFIED |
| R-17 | `docs/FINAL_REPORT.md` | Numbers cross-checked against generated outputs; Markdown only (convert if PDF/DOCX required) | VERIFIED |
| R-18 | Rule engine gates all recommendations | `assert_plan_valid` on all profiles + 150-case seeded fuzz | VERIFIED |
| R-19 | `Decision.evidence` / `policy_evidence`, report §2 | `assert_plan_valid` requires evidence for every recommendation; `test_markdown_report...` | VERIFIED |
| R-20 | `AdvisorChat` | `test_change_credit_load_updates_plan`, `test_add_interest_and_course_request`, `test_alternative_plans`, `test_why_*` | VERIFIED |
| R-21 | `Decision.reasons`, violations, unlock hints | `test_unmet_prerequisite...`, report tables | VERIFIED |

Not an engineering requirement but required for submission: filling in author names and submitting via the Google Form - **user action**.
