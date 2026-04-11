# Assignment Brief to Assignment Co-Pilot

This repository turns a Word assignment brief into a set of assignment helper artifacts you can use locally.

The public story is not "here is the final submitted file." The public story is "give the repo an assignment brief, and it produces the planning, structure, and drafting aids needed to complete the assignment responsibly."

## What It Does

- Reads an assignment `.docx` brief.
- Extracts the key metadata, requirements, and rubric signals.
- Builds an agent-style workflow for how the assignment should be executed.
- Generates an editable draft starter, figure/table plan, and Harvard citation guide.
- Keeps the final Word or PDF submission outside the public repo.
- Supports a one-command local run for any `.docx` dropped into `briefs/`.

## What It Does Not Do

- It does not produce a guaranteed grade.
- It does not auto-generate a submission-ready paper you should hand in as-is.
- It does not replace source verification, citation checking, or your own judgement.

## Repo Focus

This repo is now centered on process:

- `scripts/generate_workflow_artifacts.py`: reads a Word brief and generates workflow artifacts.
- `run_assignment_helper.py`: processes every `.docx` brief in `briefs/` with one command.
- `docs/agentic_workflow.md`: explains the agent roles and handoffs.
- `examples/`: sample outputs generated from the existing briefs in this workspace.

The legacy `prep/` workspace stays local and is ignored by Git so the public repo remains focused on workflow artifacts instead of prior assignment content.

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Drop one or more `.docx` briefs into `briefs/`, then run:

```bash
python run_assignment_helper.py
```

Or run the generator directly on specific files:

```bash
python scripts/generate_workflow_artifacts.py M511-AB-Re-Assessment-Apr-2026.docx M521-AB-Re-Assessment-Apr-2026.docx --output-dir examples
```

## Generated Artifact Set

Each brief gets its own folder with:

- `01_brief_extract.md`
- `02_brief_summary.json`
- `03_agent_workflow.md`
- `04_research_plan.md`
- `05_assignment_scaffold.md`
- `06_execution_checklist.md`
- `07_draft_starter.md`
- `08_figure_table_plan.md`
- `09_harvard_reference_guide.md`
- `10_artifact_manifest.json`

## Typical Workflow

1. Clone the repo.
2. Drop a Word brief into `briefs/`.
3. Run `python run_assignment_helper.py`.
4. Review the generated brief summary, scaffold, draft starter, and citation guide.
5. Write and verify the final assignment yourself.
6. Export the final deliverable locally without committing it.

## GitHub Hygiene

`.gitignore` is configured to keep private deliverables out of the repo, including:

- `.docx`
- `.pdf`
- the entire local `prep/` workspace

That keeps the repo focused on the workflow and artifacts rather than the final submission files.
