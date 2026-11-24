# Assignment Analysis (KBA RAG Course Advisor)

Source: `KBA_Assignment.pdf` summary supplied with the task. Deadline stated: **28 November 2026**.

## Objective
Python RAG Course Advisor recommending courses for the upcoming semester, supported by retrieved evidence, combined with deterministic rule validation.

## Requirements (IDs used in `requirement-matrix.md`)
| ID | Requirement | Source |
|---|---|---|
| R-01 | Knowledge base: course descriptions, prerequisites, credit limits, academic levels, availability, registration rules | §2.1 |
| R-02 | Use official documents if available; otherwise sample policies explicitly labelled fictional | §2 note |
| R-03 | Student profile: level, passed courses, skills, interests, preferred credit load | §2.2 |
| R-04 | RAG pipeline: parse, chunk, embed, retrieve, generate recommendations | §2.3 |
| R-05 | Python rule checking: prerequisites, credit limits, level restrictions, other rules | §2.4 |
| R-06 | Recommendation engine: eligible courses with reasons, credit hours, references, excluded courses | §2.5 |
| R-07 | AI chatbot using a pretrained LLM or API | §2.6 |
| R-08 | >= 6 synthetic profiles; different levels/backgrounds | §3 |
| R-09 | >= 1 profile with an unmet prerequisite | §3 |
| R-10 | >= 1 profile exceeding the credit limit | §3 |
| R-11 | Per test: input, retrieved evidence, accepted, rejected + reasons, final recommendation | §3 |
| R-12 | Deliverable: Python notebook (.ipynb) with complete implementation | §4 |
| R-13 | Deliverable: knowledge base | §4 |
| R-14 | Deliverable: dependencies list | §4 |
| R-15 | Deliverable: install/run instructions | §4 |
| R-16 | Deliverable: 6 test profiles with inputs and outputs | §4 |
| R-17 | Deliverable: final report (approach, data sources, enforced rules, sample result, limitations) | §4 |
| R-18 | Never recommend a course whose prerequisites/eligibility are unmet (grading emphasis) | §7 |
| R-19 | Display exact document + retrieved passage behind every recommendation (grading emphasis) | §7 |
| R-20 | Chatbot lets students ask questions, change preferences, explore alternative plans (grading emphasis) | §7 |
| R-21 | Explain why each course is recommended or rejected (grading emphasis) | §7 |

## Ambiguities and assumptions
1. **Individual vs team.** §1 says "individual", §6 says "team size: 2". Not resolved from the material; README leaves author names to fill in.
2. **No official college documents were provided**, so the KB is fictional and labelled (R-02). Swapping in real documents means adding files in the same format.
3. **Upcoming semester** is modelled as Fall or Spring per profile (today is 24 Nov 2026, so Spring 2027 is the natural next term; all test profiles use Spring).
4. **Final report format** is not specified; delivered as Markdown (`docs/FINAL_REPORT.md`). Convert to PDF/DOCX if the course requires it.
5. **Submission** is via a Google Form; not performed (needs the student's action).
6. "Pretrained LLM or API": implemented via the Anthropic API behind an interface, plus an offline fallback. A live call could not be made in the build environment (no API key); the integration is tested with fake clients only.
