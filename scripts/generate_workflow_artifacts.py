from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from docx import Document


def clean_text(text: str) -> str:
    cleaned = (
        text.replace("\xa0", " ")
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2014", "-")
        .replace("\u2013", "-")
    )
    return " ".join(cleaned.split())


def markdown_escape(text: str) -> str:
    return text.replace("|", r"\|")


def extract_document(docx_path: Path) -> tuple[list[str], list[list[list[str]]]]:
    document = Document(str(docx_path))

    paragraphs = [clean_text(paragraph.text) for paragraph in document.paragraphs]
    paragraphs = [paragraph for paragraph in paragraphs if paragraph]

    tables: list[list[list[str]]] = []
    for table in document.tables:
        rows: list[list[str]] = []
        for row in table.rows:
            cells = [clean_text(cell.text) for cell in row.cells]
            if any(cells):
                rows.append(cells)
        if rows:
            tables.append(rows)

    return paragraphs, tables


def extract_metadata(tables: list[list[list[str]]]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    if not tables:
        return metadata

    for row in tables[0]:
        if len(row) < 2:
            continue
        key = row[0].rstrip(":").strip()
        value = " ".join(cell for cell in row[1:] if cell).strip()
        if key and value:
            metadata[key] = value
    return metadata


def collect_assignment_text(tables: list[list[list[str]]]) -> str:
    selected_chunks: list[str] = []
    for table in tables[1:5]:
        for row in table:
            chunk = " ".join(cell for cell in row if cell).strip()
            if chunk:
                selected_chunks.append(chunk)
    return clean_text(" ".join(selected_chunks))


def shorten(text: str, limit: int = 240) -> str:
    trimmed = text.strip()
    if len(trimmed) <= limit:
        return trimmed
    return trimmed[: limit - 3].rstrip() + "..."


def extract_assignment_title(paragraphs: list[str], assignment_text: str) -> str:
    title_match = re.search(
        r"Assessment Title:\s*(.+?)(?=\s+Details:|\s+TASK\b|$)",
        assignment_text,
        re.IGNORECASE,
    )
    if title_match:
        return clean_text(title_match.group(1))

    heading_match = re.search(r"#\s*([^#]+?)(?=\s*##|$)", assignment_text)
    if heading_match:
        return clean_text(heading_match.group(1))

    return paragraphs[0] if paragraphs else "Assignment Brief"


def infer_expected_output(title: str) -> str:
    lowered = title.lower()
    if "strategy" in lowered or "analysis" in lowered:
        return "Critical analysis section supported by theory and evidence."
    if "reflection" in lowered:
        return "Personal reflection section with first-person insight and applied strategy."
    if "ethical" in lowered:
        return "Issue deep-dive with an ethical framework and a stronger alternative."
    if "recommend" in lowered or "action plan" in lowered or "strateg" in lowered:
        return "Action-oriented recommendations with clear steps, owners, and measures."
    return "A structured section that answers the brief directly."


def split_section_title_and_body(block: str) -> tuple[str, str]:
    trimmed = clean_text(block)
    verb_match = re.search(
        r"\b(Map|You should|Choose|Select|Identify|Evaluate|Develop|Reflect|Construct|Apply)\b",
        trimmed,
    )
    if verb_match:
        return trimmed[: verb_match.start()].strip(), trimmed[verb_match.start() :].strip()
    return trimmed, ""


def trim_section_body(text: str) -> str:
    stop_markers = [
        "Assessment Guidelines",
        "Purpose",
        "Links to module intended learning outcomes",
        "Special Instructions",
        "Additional Assessment Components",
        "Answer the Question",
    ]
    trimmed = clean_text(text)
    stop_positions = [trimmed.find(marker) for marker in stop_markers if marker in trimmed]
    stop_positions = [position for position in stop_positions if position >= 0]
    if stop_positions:
        trimmed = trimmed[: min(stop_positions)]
    return clean_text(trimmed).lstrip(":-. ")


def extract_part_sections(assignment_text: str) -> list[dict[str, str]]:
    pattern = re.compile(
        r"(Part\s+\d+\s*-\s*.*?)(?=Part\s+\d+\s*-\s*|$)",
        re.IGNORECASE | re.DOTALL,
    )
    sections: list[dict[str, str]] = []
    for block in pattern.findall(assignment_text):
        title, body = split_section_title_and_body(block)
        clean_title = clean_text(title)
        clean_body = trim_section_body(body)
        sections.append(
            {
                "title": clean_title,
                "description": shorten(clean_body),
                "expected_output": infer_expected_output(clean_title),
            }
        )
    return sections


def extract_named_sections(assignment_text: str, headings: list[str]) -> list[dict[str, str]]:
    lowered = assignment_text.lower()
    markers: list[tuple[int, str]] = []
    for heading in headings:
        position = lowered.find(heading.lower())
        if position >= 0:
            markers.append((position, heading))

    markers.sort()
    sections: list[dict[str, str]] = []
    for index, (start, heading) in enumerate(markers):
        end = markers[index + 1][0] if index + 1 < len(markers) else len(assignment_text)
        body = assignment_text[start + len(heading) : end]
        sections.append(
            {
                "title": heading,
                "description": shorten(trim_section_body(body)),
                "expected_output": infer_expected_output(heading),
            }
        )
    return sections


def extract_task_sections(assignment_text: str) -> list[dict[str, str]]:
    part_sections = extract_part_sections(assignment_text)
    if part_sections:
        return part_sections

    named_sections = extract_named_sections(
        assignment_text,
        [
            "Emotional Agility Analysis",
            "Solutions and Strategies",
            "Personal Reflection",
        ],
    )
    if named_sections:
        return named_sections

    return [
        {
            "title": "Assignment Brief",
            "description": shorten(assignment_text),
            "expected_output": "A complete response aligned to the brief and rubric.",
        }
    ]


def extract_weighted_criteria(tables: list[list[list[str]]]) -> list[dict[str, str]]:
    criteria: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    rubric_texts: list[str] = []
    for table in tables:
        table_text = clean_text(" ".join(" ".join(row) for row in table))
        lowered = table_text.lower()
        if "assessment criteria" in lowered or "following criteria" in lowered:
            rubric_texts.append(table_text)

    for rubric_text in rubric_texts:
        matches = re.findall(
            r"([A-Z][A-Za-z/'().,& -]{5,}?)\s*(?:-|:)?\s*(\d+\s*(?:%|marks))",
            rubric_text,
        )
        for criterion, weight in matches:
            clean_criterion = clean_text(criterion).rstrip(":")
            lowered = clean_criterion.lower()
            if lowered.startswith(("mark weight", "fail", "sufficient", "satisfactory", "good", "very good")):
                continue
            if "assessment criteria" in lowered:
                continue
            if "primary assessment task" in lowered:
                continue
            key = (clean_criterion, clean_text(weight))
            if key in seen:
                continue
            seen.add(key)
            criteria.append({"criterion": clean_criterion, "weight": clean_text(weight)})

    return criteria


def infer_assignment_type(metadata: dict[str, str], assignment_text: str) -> str:
    for key in ("Primary Assessment Task", "Primary Assessment Title", "Assessment Topic"):
        if key in metadata:
            return metadata[key]

    lowered = assignment_text.lower()
    if "individual report" in lowered:
        return "Individual report"
    if "individual essay" in lowered:
        return "Individual essay"
    return "Assignment"


def build_brief_extract_markdown(
    source_file: Path,
    paragraphs: list[str],
    tables: list[list[list[str]]],
) -> str:
    lines = [
        f"# Brief Extract: {source_file.name}",
        "",
        "## Paragraphs",
        "",
    ]

    for index, paragraph in enumerate(paragraphs, start=1):
        lines.append(f"{index}. {paragraph}")

    lines.extend(["", "## Tables", ""])
    for table_index, table in enumerate(tables, start=1):
        lines.append(f"### Table {table_index}")
        lines.append("")
        column_count = max(len(row) for row in table)
        header = [f"Column {idx}" for idx in range(1, column_count + 1)]
        lines.append("| " + " | ".join(header) + " |")
        lines.append("|" + "|".join([" --- " for _ in header]) + "|")
        for row in table:
            padded_row = row + [""] * (column_count - len(row))
            lines.append("| " + " | ".join(markdown_escape(cell) for cell in padded_row) + " |")
        lines.append("")

    return "\n".join(lines) + "\n"


def recommend_sources(section_title: str) -> str:
    lowered = section_title.lower()
    if "csr" in lowered or "esg" in lowered:
        return "Company sustainability reports, ESG ratings, annual reports, competitor disclosures, and core CSR/ESG theory."
    if "ethical" in lowered:
        return "Ethics literature, NGO or watchdog coverage, policy standards, and company responses."
    if "reflection" in lowered:
        return "Module theory, case incidents, and first-person reflection prompts."
    if "strategy" in lowered or "recommend" in lowered:
        return "Improvement frameworks, applied management literature, and feasibility evidence."
    return "Academic theory, public company or case evidence, and relevant comparator material."


def recommend_artifact(section_title: str) -> str:
    lowered = section_title.lower()
    if "esg" in lowered:
        return "Benchmark table plus one materiality or comparison visual."
    if "ethical" in lowered:
        return "Issue assessment table with gap analysis."
    if "reflection" in lowered:
        return "Short reflective section with named hooks and counter-practices."
    if "strategy" in lowered:
        return "Action plan table with timing and success measures."
    return "Argument map or evidence table."


def build_research_plan(summary: dict[str, object]) -> str:
    lines = [
        f"# Research Plan: {summary['title']}",
        "",
        "## Task-to-Evidence Matrix",
        "",
        "| Task section | What must be answered | Evidence to collect | Suggested artifact |",
        "| --- | --- | --- | --- |",
    ]

    for section in summary["task_sections"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    markdown_escape(section["title"]),
                    markdown_escape(section["description"]),
                    markdown_escape(recommend_sources(section["title"])),
                    markdown_escape(recommend_artifact(section["title"])),
                ]
            )
            + " |"
        )

    if summary["rubric_criteria"]:
        lines.extend(["", "## Rubric Signals", ""])
        for item in summary["rubric_criteria"]:
            lines.append(f"- {item['criterion']} ({item['weight']})")

    return "\n".join(lines) + "\n"


def build_agent_workflow(summary: dict[str, object]) -> str:
    lines = [
        f"# Agentic Workflow: {summary['title']}",
        "",
        "## Assignment Snapshot",
        "",
        f"- Source brief: `{summary['source_file']}`",
        f"- Module: {summary['module'] or 'Not detected'}",
        f"- Assessment type: {summary['assessment_type']}",
        f"- Due date: {summary['due_date'] or 'Not detected'}",
        f"- Word limit: {summary['word_limit'] or 'Not detected'}",
        f"- Submission method: {summary['submission_method'] or 'Not detected'}",
        "",
        "## Agent Sequence",
        "",
        "### 1. Brief Intake Agent",
        "- Goal: Read the Word brief and turn it into structured requirements.",
        "- Inputs: Original `.docx` brief.",
        "- Outputs: `01_brief_extract.md`, `02_brief_summary.json`.",
        "- Done when: metadata, tasks, and rubric signals are captured cleanly.",
        "",
        "### 2. Planning Agent",
        "- Goal: Convert the brief into a work plan that maps each task to evidence and deliverables.",
        "- Inputs: brief summary and rubric.",
        "- Outputs: `03_agent_workflow.md`, `04_research_plan.md`.",
        "- Done when: every task section has a matching evidence plan and artifact type.",
        "",
        "### 3. Research Agent",
        "- Goal: Gather the sources needed to answer the brief with critical depth.",
        "- Inputs: research plan and extracted task sections.",
        "- Outputs: source notes, comparison tables, and a citation-ready evidence base.",
        "- Done when: each claim in the future draft has a credible supporting source.",
        "",
        "### 4. Structure Agent",
        "- Goal: Build the final assignment skeleton before drafting.",
        "- Inputs: brief summary, research plan, and rubric weights.",
        "- Outputs: `05_assignment_scaffold.md`.",
        "- Done when: the outline reflects both the brief and the grading logic.",
        "",
        "### 5. Drafting Agent",
        "- Goal: Write the assignment section by section in markdown first.",
        "- Inputs: scaffold, research evidence, and required visuals or tables.",
        "- Outputs: working markdown draft and any section-level tables.",
        "- Done when: all brief tasks are answered directly and critically.",
        "",
        "### 6. QA Agent",
        "- Goal: Check alignment, word count, referencing, and evidence quality.",
        "- Inputs: draft, rubric, and checklist.",
        "- Outputs: `06_execution_checklist.md` plus revision notes.",
        "- Done when: the submission is ready to export locally as Word or PDF.",
        "",
        "## Task Sections",
        "",
    ]

    for section in summary["task_sections"]:
        lines.append(f"### {section['title']}")
        lines.append(f"- Brief focus: {section['description']}")
        lines.append(f"- Expected output: {section['expected_output']}")
        lines.append("")

    if summary["rubric_criteria"]:
        lines.extend(["## Rubric Priorities", ""])
        for criterion in summary["rubric_criteria"]:
            lines.append(f"- {criterion['criterion']} ({criterion['weight']})")
        lines.append("")

    lines.extend(
        [
            "## Public Repo Boundary",
            "",
            "- Commit the workflow docs, scripts, and generated planning artifacts.",
            "- Do not commit the original Word brief, final Word submission, or exported PDF.",
        ]
    )

    return "\n".join(lines) + "\n"


def build_assignment_scaffold(summary: dict[str, object]) -> str:
    assessment_type = str(summary["assessment_type"]).lower()
    include_exec_summary = "report" in assessment_type

    lines = [
        f"# Assignment Scaffold: {summary['title']}",
        "",
        f"**Module:** {summary['module'] or '[Fill module]'}",
        "",
        f"**Assessment type:** {summary['assessment_type']}",
        "",
    ]

    if include_exec_summary:
        lines.extend(
            [
                "## Executive Summary",
                "",
                "- Summarise the central argument, strongest evidence, biggest risk, and key recommendation.",
                "",
                "## List of Tables and Figures",
                "",
                "- Add any comparison tables, issue maps, or visuals used in the final report.",
                "",
            ]
        )

    lines.extend(["## Introduction", "", "- Frame the assignment, scope, and central argument.", ""])

    for section in summary["task_sections"]:
        lines.extend(
            [
                f"## {section['title']}",
                "",
                f"- Required focus: {section['description']}",
                "- Theory to integrate:",
                "- Evidence to cite:",
                f"- Suggested artifact: {recommend_artifact(section['title'])}",
                "",
            ]
        )

    if any("reflection" in section["title"].lower() for section in summary["task_sections"]):
        lines.extend(["## Reflection Close", "", "- End with what changes in your own practice.", ""])

    lines.extend(
        [
            "## Conclusion",
            "",
            "- Synthesize the full answer and restate the judgement.",
            "",
            "## Reference List",
            "",
            "- Add Harvard-style references.",
            "",
        ]
    )

    return "\n".join(lines)


def build_execution_checklist(summary: dict[str, object]) -> str:
    lines = [
        f"# Execution Checklist: {summary['title']}",
        "",
        "## Intake",
        "",
        "- [ ] Confirm the module, due date, submission format, and word count.",
        "- [ ] Extract all assignment parts from the Word brief.",
        "- [ ] Capture rubric criteria and weighting where available.",
        "",
        "## Planning",
        "",
        "- [ ] Turn every brief section into a draft section or subsection.",
        "- [ ] Identify the theories, frameworks, or models required.",
        "- [ ] Build a source list for both academic and practical evidence.",
        "",
        "## Drafting",
        "",
    ]

    for section in summary["task_sections"]:
        lines.append(f"- [ ] Complete `{section['title']}`.")

    lines.extend(
        [
            "",
            "## Quality Gate",
            "",
            "- [ ] Make sure the answer is analytical, not just descriptive.",
            "- [ ] Check that recommendations or reflections follow logically from the analysis.",
            "- [ ] Confirm Harvard referencing and citation consistency.",
            "- [ ] Check visuals, tables, and appendices for relevance.",
            "- [ ] Export the final Word or PDF locally without committing it to Git.",
            "",
        ]
    )

    return "\n".join(lines)


def build_summary(
    source_file: Path,
    paragraphs: list[str],
    tables: list[list[list[str]]],
) -> dict[str, object]:
    metadata = extract_metadata(tables)
    assignment_text = collect_assignment_text(tables)
    task_sections = extract_task_sections(assignment_text)
    rubric_criteria = extract_weighted_criteria(tables)

    title = extract_assignment_title(paragraphs, assignment_text)
    module = metadata.get("Module", "")
    due_date = metadata.get("To be submitted on", "") or metadata.get("To be submitted on:", "")
    submission_method = metadata.get("Submission Method", "")
    word_limit = metadata.get("Length", "")

    summary = {
        "source_file": source_file.name,
        "title": title,
        "module": module,
        "assessment_type": infer_assignment_type(metadata, assignment_text),
        "due_date": due_date,
        "submission_method": submission_method,
        "word_limit": word_limit,
        "task_sections": task_sections,
        "rubric_criteria": rubric_criteria,
    }
    return summary


def build_manifest(output_dir: Path) -> dict[str, object]:
    return {
        "output_dir": str(output_dir),
        "files": [
            {"name": "01_brief_extract.md", "purpose": "Human-readable extract of the input Word brief."},
            {"name": "02_brief_summary.json", "purpose": "Structured metadata, task sections, and rubric signals."},
            {"name": "03_agent_workflow.md", "purpose": "Agent roles, handoffs, and done criteria for the assignment run."},
            {"name": "04_research_plan.md", "purpose": "Task-to-evidence matrix for source collection and analysis."},
            {"name": "05_assignment_scaffold.md", "purpose": "Draft-ready section outline aligned to the brief."},
            {"name": "06_execution_checklist.md", "purpose": "Pre-submission checklist for drafting and QA."},
            {"name": "07_artifact_manifest.json", "purpose": "Machine-readable list of generated workflow artifacts."},
        ],
    }


def generate_for_brief(docx_path: Path, base_output_dir: Path) -> Path:
    paragraphs, tables = extract_document(docx_path)
    summary = build_summary(docx_path, paragraphs, tables)

    target_dir = base_output_dir / docx_path.stem
    target_dir.mkdir(parents=True, exist_ok=True)

    (target_dir / "01_brief_extract.md").write_text(
        build_brief_extract_markdown(docx_path, paragraphs, tables),
        encoding="utf-8",
    )
    (target_dir / "02_brief_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    (target_dir / "03_agent_workflow.md").write_text(
        build_agent_workflow(summary),
        encoding="utf-8",
    )
    (target_dir / "04_research_plan.md").write_text(
        build_research_plan(summary),
        encoding="utf-8",
    )
    (target_dir / "05_assignment_scaffold.md").write_text(
        build_assignment_scaffold(summary),
        encoding="utf-8",
    )
    (target_dir / "06_execution_checklist.md").write_text(
        build_execution_checklist(summary),
        encoding="utf-8",
    )

    manifest = build_manifest(target_dir)
    (target_dir / "07_artifact_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    return target_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read assignment brief .docx files and generate agentic workflow artifacts."
    )
    parser.add_argument("briefs", nargs="+", help="Path(s) to assignment brief .docx files.")
    parser.add_argument(
        "--output-dir",
        default="workflow_runs",
        help="Directory where generated artifact folders should be written.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    created_dirs: list[Path] = []

    for brief in args.briefs:
        docx_path = Path(brief)
        created_dirs.append(generate_for_brief(docx_path, output_dir))

    for directory in created_dirs:
        print(f"Generated workflow artifacts in: {directory}")


if __name__ == "__main__":
    main()
