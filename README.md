# Assignment Helper Co-Pilot

Read an assignment brief (`.docx` or `.pdf`) and produce a complete `.docx` draft with analysis, Harvard citations, references, tables, and figures — no API key, no external service.

The student rewrites the language in their own voice before submission.

---

## Quick Start

```bash
pip install -r requirements.txt
```

Drop briefs into `briefs/`, then:

```bash
python run_assignment_helper.py
```

Output goes to `workflow_runs/<brief_name>/` as a `.docx` and `.md` summary.

---

## What You Get

- **Introduction** with citations (150+ words)
- **Per-section analysis** covering every task and sub-task with framework integration and in-text citations
- **Conclusion** with synthesis and limitations
- **Tables** (comparison matrix, framework evaluation, gap analysis)
- **Matplotlib figures** (bar charts with captions)
- **10 Harvard references** matched to your topic
- **Rubric self-audit** checklist
- **Formatted .docx** — Times New Roman 12pt, 1.5 spacing, 1-inch margins, justified, page numbers

---

## How It Works

1. **Extract** — read paragraphs and tables from the brief
2. **Parse** — detect metadata, task sections, sub-tasks, rubric criteria, learning outcomes
3. **Generate** — build content using a template engine (topic detection → reference matching → framework integration → sentence assembly with citations → table/figure data)
4. **Build** — produce a formatted `.docx` with all sections, references, figures, and checklists

No LLM, no API, no network calls. Everything runs locally.

---

## Requirements

```
python-docx    pdfplumber    matplotlib    Pillow
```

---

## Important

This tool **helps produce a structured draft** — it is **not** a final submission, **not** a grade guarantee, and **not** a replacement for your own judgement. You must critically evaluate everything, rewrite the language in your own voice, and verify every source before submitting. Unmodified output may violate academic integrity policies. Use responsibly and take a license in future to avoid any problems.
