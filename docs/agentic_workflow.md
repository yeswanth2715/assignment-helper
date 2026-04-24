# Agentic Assignment Co-Pilot Workflow

This repo is organized around a repeatable workflow:

1. Input a Word or PDF assignment brief.
2. Extract the brief into structured text and metadata.
3. Convert the brief into task sections, rubric signals, and evidence needs.
4. Build planning artifacts and an editable draft starter.
5. Write and package the final submission locally, without committing the private deliverable.
6. Carry relevant workflow outputs and figures forward into the final local deliverable.

## Agent Roles

### Brief Intake Agent

- Reads the `.docx` or `.pdf` brief.
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

- Produces an editable draft starter in markdown.
- Uses the scaffold, research plan, and evidence base.
- Treats the brief as a checklist, not as permission to skip human judgement.

### QA Agent

- Checks rubric coverage, critical depth, referencing, and word count.
- Confirms that the answer is analytical rather than descriptive.
- Approves the final export to Word or PDF outside the public repo.

## Core Artifacts

- `01_brief_extract.md`: raw human-readable extract from the Word or PDF brief.
- `02_brief_summary.json`: structured summary for automation and reuse.
- `03_agent_workflow.md`: agent handoffs, responsibilities, and done criteria.
- `04_research_plan.md`: task-to-evidence matrix.
- `05_assignment_scaffold.md`: section outline with word-count allocation and LO mapping.
- `06_execution_checklist.md`: MSc-standard quality gates before submission.
- `07_draft_starter.md`: editable markdown starter with placeholders and rubric self-audit.
- `08_figure_table_plan.md`: suggested visuals and tables for the assignment.
- `09_harvard_reference_guide.md`: citation and reference templates (incl. book chapter, conference paper, government report).
- `10_artifact_manifest.json`: manifest of generated files.

## Quality Expectations (MSc Level)

The generated artifacts are designed to support postgraduate (MSc) assignment standards:

- **Word-count allocation**: the scaffold estimates a per-section word budget derived from rubric weights.
- **Learning outcome mapping**: learning outcomes are extracted from the brief and linked to scaffold sections.
- **Rubric self-audit**: the draft starter includes a checklist for verifying each rubric criterion before submission.
- **Critical-depth checklist**: the execution checklist gates for analytical (not descriptive) writing, theory integration, originality, and proofreading.
- **Diverse referencing**: the Harvard guide covers journal articles, books, book chapters, conference papers, company reports, government reports, newspaper articles, and secondary citations.
- **Differentiated evidence**: the research plan recommends specific source types per section (not generic copy-paste).

## Ethical Boundary

This repo is designed as a co-pilot, not an auto-submit engine.

- It can help structure the work.
- It can help plan sources, figures, and citations.
- It cannot guarantee grades.
- It should not be used to submit unchecked, unverified output as finished academic work.

## Public Repo Boundary

The GitHub-facing repo should center on:

- scripts
- workflow docs
- example planning artifacts
- templates and scaffolds

The repo should not center on:

- original assignment briefs in Word or PDF format
- final submitted Word or PDF files
- private grading or student-identifying details
