# Agentic Workflow: CSR, ESG, and Ethics Analysis of a Multinational Corporation (MNC)

## Assignment Snapshot

- Source brief: `M511-AB-Re-Assessment-Apr-2026.docx`
- Module: M511 CSR, ESG and Ethics
- Assessment type: Individual report
- Due date: 10 April 2026, 18:00 CET
- Word limit: Primary Assessment (70% weightage) 3,000 words +/- 10% not including Title Page, Contents Page, Executive Summary, References or Appendices
- Submission method: This assignment must be presented on a date/time indicated by the module leader and be also submitted as a MS Word or PDF File on the corresponding Submission Folder to be found on Canvas. Designated online tasks should be completed by the deadlines specified by the tutors. Do note that all tasks must be completed by the deadline applicable for the principal assessment task.

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

### Part 1 - CSR Strategy Evaluation
- Brief focus: Map the firm's CSR initiatives to one of the following theories: Carroll's CSR Pyramid Stakeholder Theory Shared Value Framework (Porter & Kramer) Critically evaluate the alignment between CSR strategy and business strategy, Scope (local...
- Expected output: Critical analysis section supported by theory and evidence.

### Part 2 - ESG Performance Analysis
- Brief focus: You should analyze the MNC's ESG performance using ESG ratings, and sustainability reports. Construct an ESG profile summarizing: Environmental performance, social performance, governance structures and policies, and finally compare the...
- Expected output: Critical analysis section supported by theory and evidence.

### Part 3 - Ethical Issue Deep Dive
- Brief focus: You should select one major ethical challenge the MNC has faced (or is currently facing) such as: supply chain labor issues, data privacy, human rights, environmental destruction, corruption or governance failures, etc., then apply one o...
- Expected output: Issue deep-dive with an ethical framework and a stronger alternative.

## Rubric Priorities

- Knowledge, understanding & depth of analysis (25 marks)
- Integration of academic theory and real-word practice (20 marks)
- Critical evaluation & argument (15 marks)
- Structure, communication & academic writing (10 marks)

## Public Repo Boundary

- Commit the workflow docs, scripts, and generated planning artifacts.
- Do not commit the original Word brief, final Word submission, or exported PDF.
