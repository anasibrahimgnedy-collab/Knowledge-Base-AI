# Final Report - KBA RAG Course Advisor

**Author:** Anas Ibrahim Mahmoud  |  **ID:** 2403245109

*Data notice: the knowledge base is fictional sample data, labelled as such in every file.*

## 1. Approach
The system is a **RAG pipeline coupled to a deterministic rule engine**, so the LLM can never invent eligibility:

1. **Parse** - Markdown documents with a `key: value` metadata header and `##` sections (`knowledge_base.py`).
2. **Chunk** - one chunk per section; sections longer than 120 words are split into overlapping windows (20 words). Each chunk keeps its source file and section, and is embedded with the document title/tags as context.
3. **Embed** - TF-IDF (unigrams + bigrams, sublinear tf, L2-normalised) by default, so the system runs fully offline and reproducibly. A pretrained `sentence-transformers` model can be plugged in through the same `Embedder` interface.
4. **Retrieve** - cosine similarity over all chunks, with filters by document type / id / section.
5. **Rule check (Python)** - structured fields from the same documents feed `RuleEngine`, which returns every violated rule for a course.
6. **Recommend** - eligible courses are scored, then packed by an exact dynamic-programming knapsack under the credit limit (see §4). Each decision carries reasons and the retrieved evidence.
7. **Chatbot** - deterministic intent handling (change load, add interest, request/remove course, "why X?", alternative plans, free questions answered from retrieved passages). A pretrained LLM, when configured, only rephrases facts supplied by the engine; ungrounded course codes cause a fallback to the template.

**Why this split:** retrieval is probabilistic and an LLM can hallucinate; prerequisites and credit caps are exact. Rules therefore gate every recommendation, retrieval supplies the citable evidence, and the LLM is a presentation layer.

## 2. Data sources
No official college documents were supplied, so a **fictional** Bachelor of Computer Science catalogue was written for this assignment (as the brief permits for unavailable policies):

* 30 course documents (levels 1-4, 1-4 credit hours, Fall/Spring availability, prerequisites, one corequisite lab, minimum-credit and minimum-GPA requirements).
* 4 policy documents: credit-load policy, prerequisite/corequisite policy, academic-level & availability policy, degree requirements/advising guidelines.

Numeric policy parameters (credit limits, GPA thresholds) live in each policy document's header and are read by the rule engine; the same numbers appear in the prose that retrieval returns as evidence (a test asserts they agree). Replacing the files with real college documents in the same format requires no code change.

## 3. Rules enforced (all in `rules.py`, all verified by tests)
| Rule | Behaviour |
|---|---|
| Already passed | A passed course is never re-registered |
| Availability | Course must be offered in the upcoming term (Fall/Spring) |
| Level restriction | Course level <= student level |
| Prerequisites | **All** listed prerequisites must be passed |
| Minimum passed credits | e.g. Capstone 60, Ethics 30 |
| Minimum GPA | e.g. Capstone 2.0, Deep Learning 2.5; missing GPA fails |
| Corequisite | Passed, or co-registered; lab fails if its corequisite is itself ineligible |
| Credit limit | GPA < 2.0 -> 12; 2.0-2.99 -> 18; >= 3.0 -> 21; no GPA (first semester) -> 18. Requested courses that would exceed it are rejected with the policy citation |
| Minimum load | Below 12 credit hours produces a warning (not a block) |

## 4. Ranking and packing
`score = 1.0·relevance + 0.45·[core course] + 0.15·[course at student's level] + 2.0·[requested]`, where *relevance* is the best chunk similarity between the student's interests/goals/skills and the course, min-max scaled to [0,1]. Ranking only orders courses that already passed every rule.
Packing is two exact knapsack phases over corequisite groups: (A) requested courses within the hard maximum (overflow rejected as `CREDIT_LIMIT_EXCEEDED`); (B) fill the planned load `min(preferred, maximum)`, maximising credit hours first, then score. An early greedy version stopped at 10 hours where 12 was achievable (found while inspecting profile 7); it was replaced by the exact method and covered by a regression test.

## 5. Test results (7 synthetic profiles, all Spring term; full output in `outputs/` and the notebook)
| # | Student | Level / GPA | Scenario | Result |
|---|---|---|---|---|
| 1 | Amira Hassan | 1 / none | New student, empty history | CS101, MATH101, ENG101, HUM101 (13/18). Fall-only CS103 rejected; CS102 etc. rejected for missing prerequisites |
| 2 | Omar Khaled | 1 / 3.2 | Requests level-2 CS204 | CS204 rejected by **level restriction**; plan CS102, MATH102, ENG101, HUM101 (12/21) |
| 3 | Layla Mansour | 2 / 3.4 | Wants machine learning | ML courses (level 3) rejected despite strong interest; plan MATH202, CS203, CS202, CS204 (13/21) |
| 4 | Youssef Adel | 3 / 3.0 | **Unmet prerequisites** (skipped CS202, MATH202) | Requested CS302 and CS304 rejected with the missing prerequisites and a hint to take CS202/MATH202 first; plan CS301, MATH202, CS202, CS307, CS204 (16/21) |
| 5 | Sara Nabil | 3 / 2.4 | **Exceeds credit limit** (wants 24, requests 22 h) | Limit 18; CS204 and CS304 rejected `CREDIT_LIMIT_EXCEEDED`; plan CS307, CS303, CS301, CS302, CS305, CS303L (16/18) |
| 6 | Nour Fathy | 4 / 3.7 | Senior, eligible for capstone | CS401, CS403, CS405, CS407, CS304, CS306 (19/21); Fall-only CS404 rejected |
| 7 | Karim Samir | 4 / 1.8 | Probation, 29 passed credits, repeat request | Limit 12; CS401 rejected (needs 60 credits and GPA 2.0); CS407 rejected (30 credits, has 29); CS101 already passed; plan CS203, MATH201, MATH202, HUM101 (12/12) |

### Sample result (profile 4, abridged)
> **Rejected - CS302 Operating Systems:** `PREREQUISITE_UNMET` - missing prerequisite(s): CS202. *Hint: take CS202 first (eligible now).*
> Evidence: `kb/courses/CS302.md § Overview` - "CS302 Operating Systems is a 3-credit-hour core course at academic level 3. It is offered in the Spring semester only. Registration requirements - prerequisites: CS201, CS202."
> Policy: `kb/policies/prerequisite_policy.md § Prerequisites` - "A student may register for a course only if every prerequisite listed for that course has been passed."

## 6. Verification
* 82 automated tests (`pytest`): knowledge-base integrity (no dangling references/cycles, fictional labels, text-vs-field agreement), retrieval, every rule and boundary, credit-limit packing, corequisites, chatbot (including LLM-hallucination and API-failure fallbacks), report content, CLI.
* A **seeded fuzz test** (150 random student histories, requests and GPAs) asserts independently of the planner that no recommended course violates a rule, no plan exceeds its credit limit, corequisites are co-registered, and every recommendation has retrieved evidence.
* `ruff` lint clean. The notebook is executed end-to-end with no errors.

## 7. Limitations
* **Fictional knowledge base** - not the real college rules; real documents would need the same header format (or a parser for their layout, e.g. PDF).
* **TF-IDF retrieval** is lexical: synonyms ("AI" vs "artificial intelligence") can be missed. It only affects *ranking and evidence selection*, never eligibility. The neural embedder is wired in but not evaluated here.
* **Live LLM path untested against the real API** (no key in the build environment); verified with fake clients, plus the offline mode which is what the notebook shows. Free-form chat answers in offline mode are retrieved passages, not synthesised prose.
* Intent parsing for chat is regex-based; unusual phrasing falls through to knowledge-base Q&A.
* Not modelled: timetable conflicts, seat capacity, failed-course retakes (failed vs passed is not distinguished), in-progress courses, "any-of" prerequisites, instructor approval, graduation audit across all semesters.
* Student level is taken as given rather than derived from passed credits.
* Packing maximises the requested-course score first, so it can leave a couple of credit hours unused (profile 5: 16 of 18) when no remaining course fits.
