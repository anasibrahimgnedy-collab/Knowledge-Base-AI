# Final Verification Record

Run from a **fresh `git clone`** in a new virtual environment (`pip install -r requirements.txt`), Python 3.13, scikit-learn 1.9.1, numpy 2.5.3.

| Check | Command | Result |
|---|---|---|
| Install | `pip install -r requirements.txt` | succeeded |
| Tests | `python -m pytest -q` | **82 passed** |
| Lint | `ruff check src tests scripts` | clean |
| Profiles | `python -m course_advisor run-profiles` | 7 profiles; regenerated `outputs/` identical to the committed files (deterministic) |
| Notebook | `python scripts/build_notebook.py` | executed, 0 error outputs, 29 cells |
| Chat CLI | piped `why CS302?` / `I want 12 credits` | grounded answers with sources |

## Test strategy (summary)
* **Unit**: parser/chunker, each rule (with boundaries), retriever filters, embedder errors, profile validation.
* **Property/invariant**: every plan (7 profiles + 150 seeded random students) satisfies - no ineligible course, within credit limit, corequisites co-registered, evidence present, rejections have reasons. These checks use `RuleEngine` directly, independent of the packing code.
* **Scenario**: required cases (unmet prerequisite, credit-limit overflow, availability, level, min credits/GPA, repeat course, probation cap).
* **Chatbot**: intents, LLM grounding guard, API-failure fallback (fake clients).
* **Consistency**: policy numbers in prose equal those parsed for the rule engine; overview text equals structured fields.

## Defects found and fixed during verification
1. Greedy packing left 10/12 credit hours with a false "too few courses" warning -> replaced with exact knapsack + regression test.
2. Chatbot "why" explanations omitted the policy citation -> fixed; caught by `test_why_rejected_cites_rule_and_source`.
3. Retrieved "Overview" evidence sometimes returned a short notes chunk; policy query for prerequisites returned the wrong section -> section filter and sharper rule queries.
4. "Alternative plans" returned a single plan silently -> now explains.

## Not verified / outstanding
* **Live LLM call** (requires `ANTHROPIC_API_KEY`; not available here). Only mocked.
* Neural (`sbert`) embedder path not exercised (optional dependency, no model download here).
* Author names, Google Form submission, and PDF/DOCX conversion of the report (if required) are for the student.
* Knowledge base is fictional; no official college documents were provided.
