# Assignment Brief to Agentic Workflow

This repository turns a Word assignment brief into a set of GitHub-friendly workflow artifacts.

The public story is not "here is the final submitted file." The public story is "give the repo an assignment brief, and it produces the planning, workflow, and execution artifacts needed to complete the assignment."

## What It Does

- Reads an assignment `.docx` brief.
- Extracts the key metadata, requirements, and rubric signals.
- Builds an agent-style workflow for how the assignment should be executed.
- Generates planning artifacts you can commit to GitHub.
- Keeps the final Word or PDF submission outside the public repo.

## Repo Focus

This repo is now centered on process:

- `scripts/generate_workflow_artifacts.py`: reads a Word brief and generates workflow artifacts.
- `docs/agentic_workflow.md`: explains the agent roles and handoffs.
- `examples/`: sample outputs generated from the existing briefs in this workspace.

The legacy `prep/` workspace stays local and is ignored by Git so the public repo remains focused on workflow artifacts instead of prior assignment content.

## Quick Start

Install dependencies:

```bash
pip install -r requirements.txt
```

Generate workflow artifacts from a new brief:

```bash
python scripts/generate_workflow_artifacts.py path/to/assignment-brief.docx --output-dir workflow_runs
```

Generate artifacts for the example briefs already in this workspace:

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
- `07_artifact_manifest.json`

## Typical Workflow

1. Drop in a Word brief.
2. Run the generator.
3. Review the extracted tasks and rubric.
4. Use the scaffold and research plan to draft the assignment.
5. Export the final deliverable locally without committing it.

## GitHub Hygiene

`.gitignore` is configured to keep private deliverables out of the repo, including:

- `.docx`
- `.pdf`
- the entire local `prep/` workspace

That keeps the repo focused on the workflow and artifacts rather than the final submission files.
