from __future__ import annotations

import json
import logging
import re
from typing import Any

from .llm_client import LLMConfig, generate

logger = logging.getLogger(__name__)


def generate_section_content(
    section_title: str,
    section_description: str,
    sub_tasks: list[str],
    summary: dict[str, Any],
    config: LLMConfig | None = None,
) -> str:
    sub_task_prompts = ""
    if sub_tasks:
        sub_task_prompts = "\n".join(f"  {i}. {t}" for i, t in enumerate(sub_tasks, 1))

    prompt = f"""Write the following section of a master's-level assignment.

Section title: {section_title}
Section requirement: {section_description}
"""
    if sub_task_prompts:
        prompt += f"""
This section contains the following sub-tasks that must all be addressed:
{sub_task_prompts}
"""
    prompt += """
Write 400-700 words of critical analysis that:
- Directly answers every sub-task listed
- Uses at least 3-4 Harvard-style in-text citations (Author, Year) from credible academic sources
- Integrates relevant theory and frameworks
- Provides critical evaluation (not just description)
- Includes specific examples, data points, or quantitative evidence
- Uses clear section structure with logical paragraph flow
- Includes at least one placeholder marker like [TABLE: description] or [FIGURE: description] where a table or figure would strengthen the argument

The language must sound natural and human-written — vary sentence structure, avoid formulaic phrases like "In conclusion" or "This essay will", and write with an authoritative academic voice.

Output only the section body text (no title repetition, no meta commentary)."""
    return generate(prompt, summary, config)


def generate_introduction(summary: dict[str, Any], config: LLMConfig | None = None) -> str:
    sections = summary.get("task_sections", [])
    section_summary = "\n".join(
        f"- {s['title']}: {s['description'][:120]}"
        for s in sections
    )
    prompt = f"""Write the introduction for a master's-level assignment.

Assignment title: {summary.get("title", "N/A")}
Module: {summary.get("module", "N/A")}
Word limit: {summary.get("word_limit", "N/A")}

Sections to be covered:
{section_summary}

Write 150-250 words that:
- Frames the topic and its significance (with a citation)
- States the specific focus/scope of the assignment
- Briefly outlines the structure
- Uses at least 2 Harvard citations

Make it natural and authoritative, not formulaic. Output only the introduction text."""
    return generate(prompt, summary, config)


def generate_conclusion(summary: dict[str, Any], config: LLMConfig | None = None) -> str:
    sections = summary.get("task_sections", [])
    section_summary = "\n".join(f"- {s['title']}" for s in sections)
    prompt = f"""Write the conclusion for a master's-level assignment.

Assignment title: {summary.get("title", "N/A")}
Sections covered:
{section_summary}

Write 150-250 words that:
- Synthesises the key findings/arguments (do not introduce new material)
- Restates the central judgement
- Acknowledges limitations
- Suggests practical implications or future directions
- Uses at least 1 Harvard citation

Make it natural and authoritative. Output only the conclusion text."""
    return generate(prompt, summary, config)


def generate_references(summary: dict[str, Any], config: LLMConfig | None = None) -> list[dict[str, str]]:
    sections = summary.get("task_sections", [])
    section_topics = "; ".join(s["title"] for s in sections)
    prompt = f"""Generate 10-12 plausible Harvard-style references relevant to this assignment.

Module: {summary.get("module", "N/A")}
Assignment title: {summary.get("title", "N/A")}
Topics covered: {section_topics}

For each reference provide:
- A real-sounding author and year (use real researchers where possible, but verify nothing)
- A real-sounding journal, book, or report title
- A brief note on what the source covers

Output as JSON array of objects with: "citation" (full Harvard format), "type" (journal/book/report), "relevance" (1 sentence)

Example:
[
  {{
    "citation": "Author, A.A. and Author, B.B. (2023) 'Article title', Journal Name, 15(3), pp. 45-67.",
    "type": "journal",
    "relevance": "Covers stakeholder theory application in CSR context."
  }}
]

Output ONLY valid JSON, no other text."""
    raw = generate(prompt, summary, config)
    try:
        refs = json.loads(raw)
        if isinstance(refs, list):
            return refs
    except json.JSONDecodeError:
        # Try extracting JSON from markdown code block
        match = re.search(r"```(?:json)?\s*\n(.+?)\n```", raw, re.DOTALL)
        if match:
            try:
                refs = json.loads(match.group(1))
                if isinstance(refs, list):
                    return refs
            except json.JSONDecodeError:
                pass
    logger.warning("Could not parse LLM reference output; using fallback template references.")
    return []


def generate_table_data(section_title: str, summary: dict[str, Any], config: LLMConfig | None = None) -> list[dict[str, Any]]:
    """Generate structured table data relevant to a section's topic."""
    prompt = f"""For the assignment section "{section_title}" in a {summary.get("module", "")} assignment titled "{summary.get("title", "")}", suggest a useful table.

The table should compare/contrast, present evidence, or map concepts.

Output as JSON:
{{
  "title": "Descriptive table title",
  "headers": ["Column1", "Column2", "Column3"],
  "rows": [["data1", "data2", "data3"], ...],
  "caption": "Table caption with source note"
}}

Include 4-6 rows of realistic-looking data. Output ONLY valid JSON."""
    raw = generate(prompt, summary, config)
    try:
        data = json.loads(raw)
        if all(k in data for k in ("headers", "rows", "caption")):
            return data
    except (json.JSONDecodeError, TypeError):
        match = re.search(r"```(?:json)?\s*\n(.+?)\n```", raw, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                if all(k in data for k in ("headers", "rows", "caption")):
                    return data
            except json.JSONDecodeError:
                pass
    return {}


def generate_figure_data(section_title: str, summary: dict[str, Any], config: LLMConfig | None = None) -> dict[str, Any]:
    """Generate structured data for a matplotlib figure."""
    prompt = f"""For the assignment section "{section_title}" in a {summary.get("module", "")} assignment titled "{summary.get("title", "")}", suggest data for a bar chart or comparison figure.

Output as JSON:
{{
  "title": "Figure title",
  "type": "bar" or "horizontal_bar",
  "labels": ["label1", "label2", "label3", "label4"],
  "values": [number, number, number, number],
  "xlabel": "X-axis label",
  "ylabel": "Y-axis label",
  "caption": "Figure caption with source note"
}}

Include 4-6 data points with realistic values. Output ONLY valid JSON."""
    raw = generate(prompt, summary, config)
    try:
        data = json.loads(raw)
        if all(k in data for k in ("labels", "values", "type")):
            return data
    except (json.JSONDecodeError, TypeError):
        match = re.search(r"```(?:json)?\s*\n(.+?)\n```", raw, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group(1))
                if all(k in data for k in ("labels", "values", "type")):
                    return data
            except json.JSONDecodeError:
                pass
    return {}
