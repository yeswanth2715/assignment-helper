# Assignment Helper Co-Pilot

Read an academic assignment brief (`.docx` or `.pdf`) and produce a structured, drafting-ready assignment package — with or without AI-generated content.

Two modes:

| Mode | Command | Output |
|---|---|---|
| **Placeholder** (no API key) | `python run_assignment_helper.py` | Scaffold, checklist, draft starter with `[fill in]` prompts, sub-task breakdown, Harvard template, figure/table plan |
| **LLM** (with API key) | `python run_assignment_helper.py --llm` | Everything above **plus** a complete `.docx` with written analysis, Harvard in-text citations, reference list, topic-appropriate tables, and matplotlib figures |

In both modes the student is expected to **humanise the language** and verify all sources before submission. The tool handles the structural scaffolding, brief coverage, rubric alignment, and formatting so you can focus on critical depth and original argument.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Pipeline Architecture](#pipeline-architecture)
- [What Gets Generated](#what-gets-generated)
  - [Without `--llm` (Placeholder mode)](#without---llm-placeholder-mode)
  - [With `--llm` (LLM mode)](#with---llm-llm-mode)
- [LLM Setup](#llm-setup)
- [Sub-Task Detection](#sub-task-detection)
- [Figures and Tables](#figures-and-tables)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Ethical Use](#ethical-use)
- [Git Hygiene](#git-hygiene)

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Drop one or more .docx or .pdf briefs into briefs/
# (the directory is gitignored so briefs stay private)

# Run in placeholder mode (no API key needed)
python run_assignment_helper.py

# Or run with LLM content generation
export OPENROUTER_API_KEY="sk-..."
python run_assignment_helper.py --llm
```

Each brief gets its own folder under `workflow_runs/` (gitignored). Open the generated `.docx` in Word or LibreOffice.

### Per-file usage

```bash
python scripts/generate_workflow_artifacts.py path/to/brief.docx --output-dir output_folder

python scripts/generate_workflow_artifacts.py path/to/brief.docx --output-dir output_folder --llm
```

### Supported input formats

- Microsoft Word (`.docx`) — via `python-docx`
- PDF (`.pdf`) — via `pdfplumber`

---

## Pipeline Architecture

```
                      ┌──────────────────┐
                      │  .docx / .pdf     │
                      │  assignment brief │
                      └────────┬─────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Document Extraction │
                    │  (paragraphs + tables)│
                    └────────┬────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │  Metadata Extraction │
                    │  Module, word limit, │
                    │  due date, method    │
                    └────────┬────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │  Task Section Parser │
                    │  (Part X, numbered   │
                    │   questions, named   │
                    │   headings, research │
                    │   paper sections)    │
                    └────────┬────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │  Sub-Task Detection  │
                    │  Splits each section │
                    │  into discrete tasks │
                    └────────┬────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
           ┌────────────────┐  ┌──────────────────┐
           │  Placeholder   │  │  LLM Content Gen  │
           │  mode          │  │  (when --llm)     │
           │                │  │                   │
           │  - Scaffold    │  │  - Intro          │
           │  - Checklist   │  │  - Per-section    │
           │  - Draft       │  │    analysis with  │
           │    starter     │  │    citations      │
           │  - Figure plan │  │  - Conclusion     │
           │  - Harvard     │  │  - References     │
           │    guide       │  │  - Tables         │
           │                │  │  - Matplotlib     │
           │                │  │    figures        │
           └────────┬───────┘  └────────┬─────────┘
                    │                   │
                    └────────┬──────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │  build_combined_docx │
                    │  Title page, fonts,  │
                    │  line spacing,       │
                    │  margins, page nums, │
                    │  rubric audit, final │
                    │  checklist           │
                    └─────────────────────┘
```

### Extraction layer (`generate_workflow_artifacts.py`)

1. **Document IO** — reads `.docx` via `python-docx` or `.pdf` via `pdfplumber`. Text is cleaned (smart quotes, Unicode bullets, non-breaking spaces → ASCII equivalents).

2. **Metadata parser** — key-value pairs from the first table (module code, word limit, due date, submission method). Falls back to regex-based extraction from paragraph text for PDFs where table structure is less reliable.

3. **Task section detector** — a multi-strategy parser that tries, in order:
   - `Part X - Title` patterns (most common in UK-style briefs)
   - Numbered research-paper structures (`1. Title`, `2. Abstract`, `3. Introduction`...)
   - Capitalised named headings auto-detected from the text
   - Known section names (brief-type-specific fallbacks)
   - Numbered question patterns (`1. Question`, `2. Question`...)

4. **Sub-task detector** — once a section is identified, its body text is split into discrete sub-task statements by detecting:
   - Sentence boundaries (`. ` + capitalised word)
   - Action-verb transitions without a period (e.g., `(Kramer) Critically evaluate...`)
   - `, and finally` / `, then` + action verb patterns

5. **Rubric parser** — extracts weighted criteria from assessment-criteria tables. Supports both `N marks` and `N%` formats. Falls back to unweighted grading criteria from multi-column grading tables.

6. **Learning outcome extractor** — finds `LO1:`, `LO2:` patterns in tables or paragraph text.

### Generation layer

In **placeholder mode**, the tool produces planning artifacts only. In **LLM mode**, the `_generate_full_content()` function calls the LLM once per section, once for the introduction, once for the conclusion, and once for the reference list — each with a structured prompt that includes the section's description, sub-tasks, rubric criteria, and learning outcomes.

---

## What Gets Generated

### Without `--llm` (Placeholder mode)

Output folder structure (under `workflow_runs/<brief_name>/`):

| File | Content |
|---|---|
| `<brief>_helper.docx` | Single `.docx` with title page, word budget table, LO mapping, section-by-section draft starter with `###` sub-task headings, placeholders for theory/evidence/judgement per sub-task, rubric self-audit, and final submission checklist |
| `<brief>_summary.md` | Short markdown summary of metadata, sections detected, LOs, and rubric criteria |

The `.docx` also contains:
- **Introduction** — placeholder guidance
- **Each task section** — `## Section Title` with `### N. Sub-task` headings, each with a `[Answer this sub-task directly]` prompt, plus section-level slots for judgement, theory, evidence (3 sources), paragraph plan (4 paragraphs), and citation slots
- **Conclusion** — placeholder guidance
- **Reference list** — Harvard format templates (journal, book, chapter, web/report)
- **Rubric self-audit** — checkbox for every detected criterion
- **Final checks** — 7-item pre-submission checklist

### With `--llm` (LLM mode)

The same `.docx` but with **real written content** replacing every placeholder:

| Component | What the LLM generates |
|---|---|
| **Introduction** | 150–250 words framing the topic, scope, and structure with 2+ Harvard citations |
| **Each task section** | 400–700 words of critical analysis per section, covering all sub-tasks, with 3–4 in-text citations, integrated theory, critical evaluation, and specific examples |
| **Conclusion** | 150–250 words synthesising findings, restating the central judgement, acknowledging limitations |
| **Tables** | 1 topic-relevant table per section (comparison matrix, evidence map, framework summary) with Harvard-style source notes |
| **Figures** | Up to 3 matplotlib bar/horizontal-bar charts with LLM-suggested data, labels, captions |
| **References** | 10–12 Harvard-formatted references with relevance annotations, covering journals, books, chapters, and reports |

The student then **humanises the prose** — paraphrases LLM-generated sentences, varies sentence structure, removes formulaic transitions — before submission.

---

## LLM Setup

The `--llm` flag requires one of these environment variables:

| Variable | Default model | Provider |
|---|---|---|
| `OPENROUTER_API_KEY` | `openai/gpt-4o` | [OpenRouter](https://openrouter.ai) (recommended — one key, many models) |
| `OPENAI_API_KEY` | `gpt-4o` | [OpenAI](https://platform.openai.com/api-keys) |
| `ANTHROPIC_API_KEY` | `claude-sonnet-4-20250514` | [Anthropic](https://console.anthropic.com) |

Optional overrides:

```bash
export LLM_MODEL="anthropic/claude-3.5-sonnet"   # only for OpenRouter
export LLM_BASE_URL="https://custom.endpoint/v1"
```

### How the prompts work

Each section gets a dedicated system prompt that includes:
- Module code, assessment type, word limit
- Full rubric criteria with mark weights
- Learning outcomes
- Writing instructions (formal academic English, Harvard citations, critical evaluation)

The section-specific user prompt includes:
- Section title and description
- Each sub-task bullet
- Instructions for length, citation count, and output format

All prompts instruct the model to write natural, varied prose to reduce the humanisation burden.

---

## Sub-Task Detection

The sub-task parser (`extract_sub_tasks()` in `generate_workflow_artifacts.py`) decomposes a section's body text into discrete work items. For example, given:

> *Part 1 - CSR Strategy Evaluation: Map the firm's CSR initiatives to Carroll's Pyramid. Critically evaluate the alignment between CSR and business strategy. Analyze the transparency and credibility of disclosures.*

It produces three sub-tasks:

```
### 1. Map the firm's CSR initiatives to Carroll's Pyramid
### 2. Critically evaluate the alignment between CSR and business strategy
### 3. Analyze the transparency and credibility of disclosures
```

Detection works by finding:
- **Sentence boundaries** (`. ` + capitalised word) — most common in well-written briefs
- **Action-verb transitions** — when a new action verb follows a closing parenthesis or comma without a period (e.g., `(Porter & Kramer) Critically evaluate`)
- **`and finally` / `then` + verb** — catches sequential task descriptions within a single sentence

The sub-task headings appear in both the scaffold and the draft starter at the `###` level, ensuring every sub-requirement has a dedicated answer slot.

---

## Figures and Tables

### In LLM mode

The content generator calls the LLM with structured JSON prompts for each section:
- `generate_table_data()` — returns `{"headers": [...], "rows": [[...], ...], "caption": "..."}`
- `generate_figure_data()` — returns `{"type": "bar"|"horizontal_bar", "labels": [...], "values": [...], "title": "...", "caption": "..."}`

The `render_figure_from_data()` function in `generate_workflow_artifacts.py` renders these as matplotlib `.png` images that are embedded in the `.docx`. Figures are saved to a `figures/` directory next to the output.

### In placeholder mode

The draft starter includes `[TABLE: description]` and `[FIGURE: description]` markers where the LLM would normally insert visuals, signalling to the student that a table or figure would strengthen the argument at that point.

---

## Project Structure

```
├── briefs/                          # Drop .docx / .pdf briefs here (gitignored)
├── docs/
│   └── agentic_workflow.md          # 6-agent workflow documentation
├── scripts/
│   ├── __init__.py
│   ├── generate_workflow_artifacts.py  # Core: extraction, parsing, generation (1900+ lines)
│   ├── llm_client.py                   # LLM abstraction (OpenAI, Anthropic, OpenRouter)
│   └── content_generator.py            # LLM prompts for intro, sections, refs, tables, figures
├── tests/
│   └── test_generate_workflow_artifacts.py  # 31 pytest tests
├── run_assignment_helper.py          # Batch entry point
├── requirements.txt
├── .gitignore
└── README.md
```

### Key file details

**`scripts/generate_workflow_artifacts.py`** (core engine)
- `extract_document()` / `extract_pdf_document()` — reads Word/PDF into paragraphs and tables
- `extract_metadata()` / `extract_metadata_from_paragraphs()` — pulls module, length, due date
- `extract_task_sections()` — dispatcher for 4 extraction strategies
- `extract_sub_tasks()` — decomposes a section body into sub-task statements
- `extract_weighted_criteria()` — parses rubric tables for marks/percentages
- `extract_learning_outcomes()` — finds LO1/LO2/LO3 patterns
- `build_summary()` — assembles all extracted data into a structured dict
- `build_combined_docx()` — produces the final `.docx` (title page, word budget, sections with sub-tasks, rubric audit, checklist)
- `build_assignment_scaffold()` — markdown scaffold with sub-task breakdown
- `build_draft_starter()` — markdown draft starter with sub-task headings and placeholders
- `_generate_full_content()` — orchestrates LLM calls for all sections
- `render_figure_from_data()` — renders matplotlib figures from structured data
- `generate_for_brief()` — main pipeline entry point

**`scripts/llm_client.py`**
- `LLMConfig` — dataclass holding provider, model, API key, base URL, temperature
- `LLMConfig.from_env()` — auto-detects provider from env vars
- `generate()` — dispatches to OpenAI-compatible or Anthropic API

**`scripts/content_generator.py`**
- `generate_section_content()` — writes 400–700 words per section with citations
- `generate_introduction()` / `generate_conclusion()` — bookend sections
- `generate_references()` — produces 10–12 Harvard references as JSON
- `generate_table_data()` / `generate_figure_data()` — structured JSON for visuals

---

## Configuration

| Setting | Environment variable | Default |
|---|---|---|
| LLM API key | `OPENROUTER_API_KEY`, `OPENAI_API_KEY`, or `ANTHROPIC_API_KEY` | — |
| Model override | `LLM_MODEL` | Provider-dependent (see above) |
| Custom endpoint | `LLM_BASE_URL` | Provider default |
| LLM temperature | (hardcoded) | 0.7 |
| Max tokens per call | (hardcoded) | 4096 |

---

## Ethical Use

This tool is a **planning and drafting aid**, not a submission generator.

- **Placeholder mode**: Produces scaffolds and prompts. The student writes everything.
- **LLM mode**: Produces draft text that the student must **rewrite in their own voice** before submission. Most universities treat unmodified AI-generated text as academic misconduct.

The system prompt explicitly instructs the LLM to write natural, varied prose to reduce mechanical phrasing, but **final verification of every citation, claim, and argument** remains the student's responsibility.

### What the student must do

1. **Humanise** — paraphrase LLM-generated sections to match their own academic voice
2. **Verify citations** — check every (Author, Year) against the real source; LLMs hallucinate references
3. **Add original critique** — the tool prompts for evaluative thinking but cannot replace it
4. **Check word count** — the LLM estimates lengths but final trimming is manual
5. **Run Turnitin** — ensure similarity is within your institution's acceptable range

---

## Git Hygiene

The `.gitignore` keeps private content out of the public repo:

```
.doc x
.pdf
workflow_runs/
prep/
__pycache__/
.venv/
```

- **Briefs** stay in `briefs/` but are gitignored so only you see them
- **Generated outputs** go to `workflow_runs/` (gitignored)
- **API keys** are never stored in files — only read from environment variables
- The only things committed are scripts, tests, documentation, and templates

This means the repo can be public on GitHub without exposing any assignment content, API credentials, or submission files.
