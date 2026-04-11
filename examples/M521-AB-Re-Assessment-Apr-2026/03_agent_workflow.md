# Agentic Workflow: Leading Through Change: Emotional Agility at Horizon Media

## Assignment Snapshot

- Source brief: `M521-AB-Re-Assessment-Apr-2026.docx`
- Module: M521 Emotional Agility in International Business
- Assessment type: Individual Essay
- Due date: 10 April 2026, 18:00 Central European Time.
- Word limit: 3,000 words +/- 10% not including Title Page, Contents Page, Executive Summary, References or Appendices
- Submission method: The Primary Assessment must be submitted as a PDF File to the corresponding Submission Folder on Canvas.

## Agent Sequence

### 1. Brief Intake Agent
- Goal: Read the Word brief and turn it into structured requirements.
- Inputs: Original `.docx` brief.
- Outputs: `01_brief_extract.md`, `02_brief_summary.json`.
- Done when: metadata, tasks, and rubric signals are captured cleanly.

### 2. Planning Agent
- Goal: Convert the brief into a work plan that maps each task to evidence and deliverables.
- Inputs: brief summary and rubric.
- Outputs: `03_agent_workflow.md`, `04_research_plan.md`.
- Done when: every task section has a matching evidence plan and artifact type.

### 3. Research Agent
- Goal: Gather the sources needed to answer the brief with critical depth.
- Inputs: research plan and extracted task sections.
- Outputs: source notes, comparison tables, and a citation-ready evidence base.
- Done when: each claim in the future draft has a credible supporting source.

### 4. Structure Agent
- Goal: Build the final assignment skeleton before drafting.
- Inputs: brief summary, research plan, and rubric weights.
- Outputs: `05_assignment_scaffold.md`.
- Done when: the outline reflects both the brief and the grading logic.

### 5. Drafting Agent
- Goal: Write the assignment section by section in markdown first.
- Inputs: scaffold, research evidence, and required visuals or tables.
- Outputs: working markdown draft and any section-level tables.
- Done when: all brief tasks are answered directly and critically.

### 6. QA Agent
- Goal: Check alignment, word count, referencing, and evidence quality.
- Inputs: draft, rubric, and checklist.
- Outputs: `06_execution_checklist.md` plus revision notes.
- Done when: the submission is ready to export locally as Word or PDF.

## Task Sections

### Emotional Agility Analysis
- Brief focus: Identify specific emotional hooks and thought patterns affecting her leadership Evaluate how her relationship with difficult emotions impacts her effectiveness Analyze the role of values and identity in her leadership transition
- Expected output: Critical analysis section supported by theory and evidence.

### Solutions and Strategies
- Brief focus: Develop specific strategies for building emotional agility in leadership transitions Propose approaches for managing identity challenges in role transitions Create an action plan for developing psychological flexibility
- Expected output: Action-oriented recommendations with clear steps, owners, and measures.

### Personal Reflection
- Brief focus: Reflect on your own emotional patterns and hooks in professional contexts Analyze how your relationship with difficult emotions could influence your leadership Discuss your personal strategies for developing emotional agility
- Expected output: Personal reflection section with first-person insight and applied strategy.

## Rubric Priorities

- Presentation/interpretation of the case study's profile (20%)
- Integration of academic theory and 'real-world' practice (15%)
- Depth of analysis and self-reflection (15%)
- Constructing recommendations that follow logically from your critical analysis (10%)
- Quality of the proposed actions (5%)
- Professional formatting and Harvard referencing (5%)

## Public Repo Boundary

- Commit the workflow docs, scripts, and generated planning artifacts.
- Do not commit the original Word brief, final Word submission, or exported PDF.
