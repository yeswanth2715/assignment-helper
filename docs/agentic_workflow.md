# Agentic Assignment Workflow

This repo is organized around a repeatable workflow:

1. Input a Word assignment brief.
2. Extract the brief into structured text and metadata.
3. Convert the brief into task sections, rubric signals, and evidence needs.
4. Build planning artifacts before drafting.
5. Draft and package the final submission locally, without committing the private deliverable.

## Agent Roles

### Brief Intake Agent

- Reads the `.docx` brief.
- Extracts module, deadline, word count, submission method, task sections, and rubric hints.
- Produces a clean markdown extract and a machine-readable summary.

### Planning Agent

- Turns the brief into a sequence of work packages.
- Maps each assignment section to the evidence and frameworks it needs.
- Defines the artifact set required for drafting.

### Research Agent

- Gathers academic and professional sources.
- Builds source notes, comparison tables, and issue maps.
- Keeps evidence aligned to the rubric instead of collecting sources randomly.

### Structure Agent

- Converts the plan into the actual assignment skeleton.
- Decides where visuals, tables, and reflective sections belong.
- Makes the future drafting pass faster and more consistent.

### Drafting Agent

- Writes the answer in markdown first.
- Uses the scaffold, research plan, and evidence base.
- Treats the brief as a checklist, not just background context.

### QA Agent

- Checks rubric coverage, critical depth, referencing, and word count.
- Confirms that the answer is analytical rather than descriptive.
- Approves the final export to Word or PDF outside the public repo.

## Core Artifacts

- `01_brief_extract.md`: raw human-readable extract from the Word brief.
- `02_brief_summary.json`: structured summary for automation and reuse.
- `03_agent_workflow.md`: agent handoffs, responsibilities, and done criteria.
- `04_research_plan.md`: task-to-evidence matrix.
- `05_assignment_scaffold.md`: section outline for drafting.
- `06_execution_checklist.md`: quality gate before submission.
- `07_artifact_manifest.json`: manifest of generated files.

## Public Repo Boundary

The GitHub-facing repo should center on:

- scripts
- workflow docs
- example planning artifacts
- templates and scaffolds

The repo should not center on:

- original assignment briefs in Word format
- final submitted Word or PDF files
- private grading or student-identifying details
