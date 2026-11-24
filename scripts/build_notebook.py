"""Build and execute notebooks/KBA_Course_Advisor.ipynb (run from the repository root)."""
from pathlib import Path

import nbformat as nbf
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
nb = nbf.v4.new_notebook()
md = lambda t: nb.cells.append(nbf.v4.new_markdown_cell(t))  # noqa: E731
code = lambda t: nb.cells.append(nbf.v4.new_code_cell(t))  # noqa: E731

md("""# KBA Course Advisor - RAG + Deterministic Rule Engine

**What this notebook demonstrates**

| Stage | Module (`src/course_advisor/`) |
|---|---|
| Knowledge base: parse -> chunk | `knowledge_base.py` |
| Embeddings + retrieval | `embeddings.py`, `retriever.py` |
| Rule checking (Python, no LLM) | `rules.py` |
| Recommendation engine | `recommender.py` |
| Chatbot (pretrained LLM optional) | `chatbot.py`, `llm.py` |
| Report rendering | `report.py` |

> **Data notice:** no official college documents were available, so the knowledge base in `kb/` is **fictional sample data**; every file is labelled as such.

**Design principle:** the LLM never decides eligibility. Python rules decide; retrieval supplies the evidence shown to the student; the LLM (when configured) only phrases the answer from those facts.""")

code("""import sys, json, textwrap
from pathlib import Path
ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(ROOT / "src"))
from IPython.display import Markdown, display
from course_advisor import config
from course_advisor.knowledge_base import load_documents, chunk_documents, build_courses
from course_advisor.recommender import Advisor
from course_advisor.profiles import load_all_profiles
from course_advisor.report import plan_markdown
from course_advisor.models import Verdict
print("project root:", ROOT)""")

md("## 1. Knowledge base: document parsing and chunking")
code("""docs = load_documents()
chunks = chunk_documents(docs)
print(f"{len(docs)} documents ({sum(d.doc_type=='course' for d in docs)} courses, "
      f"{sum(d.doc_type=='policy' for d in docs)} policies) -> {len(chunks)} chunks")
print("\\n--- raw file: kb/courses/CS304.md ---")
print((config.COURSES_DIR / "CS304.md").read_text())""")
code("""print("--- parsed metadata (drives the rule engine) ---")
doc = next(d for d in docs if d.doc_id == "CS304")
print(json.dumps(doc.metadata, indent=2))
print("\\n--- chunks produced from this document ---")
for c in chunks:
    if c.doc_id == "CS304":
        print(f"{c.chunk_id:10} [{c.section}] {c.text[:110]}...")
print("\\n--- a policy file is chunked by section too ---")
for c in chunks:
    if c.doc_id == "POL-CREDIT":
        print(f"{c.chunk_id:12} [{c.section}] {c.text[:100]}...")""")

md("## 2. Embeddings and retrieval\nDefault embedder: TF-IDF (unigrams+bigrams, cosine similarity) - runs offline. A pretrained `sentence-transformers` model can be swapped in with `Advisor.from_knowledge_base(make_embedder('sbert'))`.")
code("""advisor = Advisor.from_knowledge_base()
print("embedder:", advisor.retriever.embedder.name, "| matrix:", advisor.retriever.matrix.shape)
for q in ["machine learning and neural networks", "maximum credit hours for a student on probation"]:
    print(f"\\nQUERY: {q}")
    for h in advisor.retriever.retrieve(q, 3):
        print(f"  {h.score:.2f}  {h.chunk.source_file} § {h.chunk.section}")""")

md("## 3. Rule engine (deterministic Python)\nThe rules read structured fields parsed from the same documents the retriever indexes.")
code("""from course_advisor.models import StudentProfile
demo = StudentProfile("Demo", level=2, term="Spring", passed_courses=["CS101","CS102","MATH101","CS103"], gpa=2.9)
for code_ in ["CS201", "CS304", "CS206", "CS101", "CS303L"]:
    v = advisor.rules.violations(demo, code_)
    print(f"{code_:7}", "ELIGIBLE" if not v else "; ".join(f"{x.rule.value}: {x.message}" for x in v))
print("\\nmax credits:", advisor.rules.max_credits(demo))""")

md("## 4. Test profiles\nSeven synthetic students (`profiles/*.json`): levels 1-4, one with **unmet prerequisites** (Youssef), one that **exceeds the credit limit** (Sara), and edge cases (Karim). For each: input, retrieved evidence, accepted courses, rejected courses with reasons, final recommendation.")
code("""profiles = load_all_profiles()
plans = [advisor.plan(p) for p in profiles]
import pandas as pd
display(pd.DataFrame([{"student": p.name, "level": p.level, "GPA": p.gpa, "preferred": p.preferred_credits,
                       "limit": pl.max_credits, "total": pl.total_credits, "recommended": ", ".join(pl.selected),
                       "rejected": sum(d.verdict is Verdict.REJECTED for d in pl.decisions.values())}
                      for p, pl in zip(profiles, plans)]))""")
for i in range(7):
    md(f"### Profile {i+1}")
    code(f"display(Markdown(plan_markdown(plans[{i}], advisor.courses)))")

md("## 5. Chatbot\nThe chatbot parses preference changes deterministically, re-runs the rule engine, and (if `ANTHROPIC_API_KEY` is set) lets a pretrained LLM phrase the reply from the grounded facts. If the LLM mentions a course that is not in the facts, the reply is discarded and the grounded template is used. Below it runs in offline template mode.")
code("""from course_advisor.chatbot import AdvisorChat
from course_advisor.llm import default_llm
llm = default_llm()
print("LLM:", llm.name if llm else "none (offline grounded-template mode)")
chat = AdvisorChat(advisor, profiles[3], llm)      # Youssef: unmet prerequisites
for msg in ["Why can't I take CS302?", "I want 12 credits", "I am interested in cybersecurity",
            "show me alternative plans", "What is the maximum number of credits on probation?"]:
    r = chat.handle(msg)
    print(f"\\nSTUDENT: {msg}\\nADVISOR: {r.text}")
    if r.sources: print("SOURCES:", "; ".join(r.sources))""")

md("## 6. Verification\nThe automated suite (`pytest`, 80+ tests) checks the invariants independently of the planner, including a seeded fuzz over random student histories: no recommended course ever violates a rule, the credit limit is never exceeded, and every recommendation has retrieved evidence.")
code("""import subprocess
res = subprocess.run([sys.executable, "-m", "pytest", "-q", "--color=no", "-p", "no:cacheprovider"], cwd=ROOT, capture_output=True, text=True)
print(res.stdout[-600:])""")

nbf.write(nb, ROOT / "notebooks" / "KBA_Course_Advisor.ipynb")
NotebookClient(nb, timeout=300, resources={"metadata": {"path": str(ROOT / "notebooks")}}).execute()
nbf.write(nb, ROOT / "notebooks" / "KBA_Course_Advisor.ipynb")
print("notebook executed and saved")
