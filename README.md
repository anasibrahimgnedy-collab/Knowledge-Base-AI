# KBA Course Advisor - RAG + Deterministic Rule Engine

A Python course-registration advisor for the KBA assignment. It is **not** just an LLM chatbot:

```
Student profile ─► RAG pipeline ─► Retrieved evidence ─┐
 (level, passed     parse → chunk →                    ├─► Recommendation engine ─► Accepted / rejected
  courses, GPA,     embed → retrieve                   │    (ranking + credit-limit     courses, reasons,
  interests, load)                                     │     packing + explanations)    credit hours, sources
                    Knowledge base (kb/)               │            ▲                          │
                    courses + policies ──► Rule engine ┘  (prerequisites, level, availability, ▼
                                           (pure Python)   credit limit, min credits/GPA, coreqs)  Chatbot (LLM optional)
```

* **Rules decide, retrieval explains, the LLM only phrases.** A course is recommended only if pure-Python rules pass.
* Every accepted/rejected course is shown with the **retrieved passage and source file** behind it.
* **Data notice:** no official college documents were available, so everything in `kb/` is **fictional sample data**, labelled as such in every file.

## Repository layout

| Path | Purpose |
|---|---|
| `notebooks/KBA_Course_Advisor.ipynb` | **Main deliverable** - executed notebook (all stages + 7 profiles + chatbot demo) |
| `kb/courses/*.md`, `kb/policies/*.md` | Knowledge base: 30 course documents, 4 policy documents |
| `src/course_advisor/` | Implementation (parsing, chunking, embeddings, retrieval, rules, recommender, chatbot, reports) |
| `profiles/profile_*.json` | 7 synthetic student profiles (test inputs) |
| `outputs/profile_*.md / .json` | Generated results for each profile (evidence, accepted, rejected, final plan) |
| `tests/` | 82 automated tests |
| `docs/` | Final report, requirement analysis/traceability matrix, verification record |
| `requirements.txt`, `pyproject.toml` | Dependencies |

## Install

Requires Python 3.10+ (developed on 3.13).

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
# 1. Open the notebook (main deliverable; outputs are already saved in it)
jupyter notebook notebooks/KBA_Course_Advisor.ipynb

# 2. Run all 7 test profiles from the command line (writes outputs/)
PYTHONPATH=src python -m course_advisor run-profiles          # Windows PowerShell: $env:PYTHONPATH="src"

# 3. Chat with the advisor as one of the profiles
PYTHONPATH=src python -m course_advisor chat profiles/profile_04.json

# 4. Tests and lint
python -m pytest -q
ruff check src tests scripts          # optional: pip install ruff

# 5. Rebuild + re-execute the notebook
python scripts/build_notebook.py
```

Example chat questions: `show my plan`, `why CS302?`, `I want 12 credits`, `I am interested in cybersecurity`,
`add CS204`, `remove CS204`, `show alternative plans`, `what is the credit limit on probation?`

### Optional: pretrained LLM
The chatbot works offline with grounded templates. To let a pretrained LLM phrase the replies:

```bash
pip install anthropic
export ANTHROPIC_API_KEY=...           # never commit this; .env is git-ignored
export ADVISOR_LLM_MODEL=claude-sonnet-5-5   # optional override
```
The LLM receives only the rule-engine verdicts and retrieved passages. If it mentions any course not in those facts,
or the API fails, the reply is discarded and the grounded template is used instead.
For neural embeddings: `pip install sentence-transformers`, then `Advisor.from_knowledge_base(make_embedder("sbert"))`.

## Adding knowledge
Add a Markdown file under `kb/courses/` (copy any existing one: `key: value` header, then `## Overview`, `## Description`, ...).
The rule engine and retriever pick it up automatically; `tests/test_knowledge_base.py` validates references and cycles.

## Author
Anas Ibrahim Mahmoud (ID 2403245109).
(The brief states both "individual" and "team size: 2"; see `docs/assignment-analysis.md`. Add a second team member here if applicable.)
