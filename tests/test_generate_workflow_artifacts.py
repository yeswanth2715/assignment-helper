"""Unit tests for generate_workflow_artifacts.py helper functions."""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from scripts.generate_workflow_artifacts import (
    clean_text,
    shorten,
    extract_metadata,
    extract_weighted_criteria,
    word_count_budget,
    extract_learning_outcomes,
    recommend_sources,
    build_harvard_reference_guide,
    build_execution_checklist,
    build_assignment_scaffold,
    build_draft_starter,
    infer_expected_output,
    generate_for_brief,
)


# ── clean_text ─────────────────────────────────────────────────────────

class TestCleanText:
    def test_collapses_whitespace(self):
        assert clean_text("hello   world") == "hello world"

    def test_replaces_smart_quotes(self):
        assert clean_text("\u201chello\u201d") == '"hello"'

    def test_replaces_bullet(self):
        assert clean_text("\u2022 item") == "- item"

    def test_replaces_trademark(self):
        assert clean_text("Brand\u2122") == "Brand(TM)"


# ── shorten ────────────────────────────────────────────────────────────

class TestShorten:
    def test_below_limit_unchanged(self):
        assert shorten("short text") == "short text"

    def test_above_limit_truncated(self):
        long_text = "a" * 600
        result = shorten(long_text)
        assert len(result) <= 500
        assert result.endswith("...")

    def test_custom_limit(self):
        result = shorten("hello world", limit=8)
        assert len(result) <= 8
        assert result.endswith("...")

    def test_strips_whitespace(self):
        assert shorten("  padded  ") == "padded"


# ── extract_metadata ──────────────────────────────────────────────────

class TestExtractMetadata:
    def test_basic_metadata(self):
        tables = [
            [
                ["Module", "M511 CSR, ESG and Ethics"],
                ["Length", "3,000 words +/- 10%"],
                ["To be submitted on", "10 April 2026"],
            ]
        ]
        meta = extract_metadata(tables)
        assert meta["Module"] == "M511 CSR, ESG and Ethics"
        assert meta["Length"] == "3,000 words +/- 10%"
        assert meta["To be submitted on"] == "10 April 2026"

    def test_empty_tables(self):
        assert extract_metadata([]) == {}


# ── extract_weighted_criteria ─────────────────────────────────────────

class TestExtractWeightedCriteria:
    def test_parses_marks_criteria(self):
        tables = [
            [
                ["Assessment Criteria",
                 "Knowledge, understanding & depth of analysis - 25 marks "
                 "Integration of academic theory and real-world practice - 20 marks"]
            ]
        ]
        criteria = extract_weighted_criteria(tables)
        assert len(criteria) >= 1
        names = [c["criterion"] for c in criteria]
        assert any("Integration" in n for n in names)

    def test_parses_percentage_criteria(self):
        tables = [
            [
                ["Assessment Criteria for the Primary Assessment Task",
                 "Presentation/interpretation of the case study's profile 20% "
                 "Integration of academic theory and 'real-world' practice 15%"]
            ]
        ]
        criteria = extract_weighted_criteria(tables)
        assert len(criteria) >= 1


# ── word_count_budget ─────────────────────────────────────────────────

class TestWordCountBudget:
    def test_with_rubric_weights(self):
        criteria = [
            {"criterion": "Knowledge", "weight": "25 marks"},
            {"criterion": "Theory", "weight": "20 marks"},
            {"criterion": "Critical eval", "weight": "15 marks"},
            {"criterion": "Structure", "weight": "10 marks"},
        ]
        budget = word_count_budget("3,000 words +/- 10%", criteria, 3)
        assert len(budget) > 0
        total = sum(w for _, w in budget)
        # Should be close to 3000 (rounding imprecision OK)
        assert 2800 <= total <= 3200

    def test_no_word_limit(self):
        assert word_count_budget("Not specified", [], 3) == []

    def test_even_distribution_no_weights(self):
        budget = word_count_budget("3,000 words", [], 3)
        assert len(budget) == 5  # intro + 3 sections + conclusion


# ── extract_learning_outcomes ─────────────────────────────────────────

class TestExtractLearningOutcomes:
    def test_extracts_los(self):
        tables = [
            [
                ["LO1: Evaluate organisations and ethical issues.",
                 "LO2: Analyse the changing nature of business."]
            ]
        ]
        los = extract_learning_outcomes(tables)
        assert len(los) == 2
        assert "LO1" in los[0]
        assert "LO2" in los[1]

    def test_no_los(self):
        tables = [[["No learning outcomes here."]]]
        assert extract_learning_outcomes(tables) == []


# ── recommend_sources ─────────────────────────────────────────────────

class TestRecommendSources:
    def test_csr_specific(self):
        result = recommend_sources("CSR Strategy Evaluation")
        assert "Carroll" in result

    def test_esg_specific(self):
        result = recommend_sources("ESG Performance Analysis")
        assert "MSCI" in result or "GRI" in result

    def test_ethical_specific(self):
        result = recommend_sources("Ethical Issue Deep Dive")
        assert "Crane" in result

    def test_emotional_agility(self):
        result = recommend_sources("Emotional Agility Analysis")
        assert "David" in result


# ── build_harvard_reference_guide ─────────────────────────────────────

class TestBuildHarvardReferenceGuide:
    def test_includes_new_source_types(self):
        guide = build_harvard_reference_guide()
        assert "Book Chapter" in guide
        assert "Conference Paper" in guide
        assert "Government" in guide
        assert "Newspaper" in guide
        assert "Secondary citation" in guide


# ── build_execution_checklist ─────────────────────────────────────────

class TestBuildExecutionChecklist:
    def test_msc_quality_gates(self):
        summary = {
            "title": "Test",
            "task_sections": [{"title": "Section 1"}],
            "rubric_criteria": [],
            "learning_outcomes": ["LO1: Test outcome."],
            "word_limit": "3,000 words",
        }
        checklist = build_execution_checklist(summary)
        assert "MSc Standard" in checklist
        assert "Word count" in checklist or "word count" in checklist.lower()
        assert "Turnitin" in checklist
        assert "LO1" in checklist
        assert "learning outcome" in checklist.lower()


# ── build_assignment_scaffold ─────────────────────────────────────────

class TestBuildAssignmentScaffold:
    def test_includes_word_budget(self):
        summary = {
            "title": "Test",
            "module": "Test Module",
            "assessment_type": "Individual report",
            "task_sections": [{"title": "Part 1", "description": "Do stuff"}],
            "rubric_criteria": [{"criterion": "Knowledge", "weight": "25 marks"}],
            "learning_outcomes": ["LO1: Test."],
            "word_limit": "3,000 words",
        }
        scaffold = build_assignment_scaffold(summary)
        assert "Word-Count Allocation" in scaffold
        assert "Learning Outcomes Addressed" in scaffold
        assert "LO1" in scaffold


# ── build_draft_starter ───────────────────────────────────────────────

class TestBuildDraftStarter:
    def test_includes_rubric_self_audit(self):
        summary = {
            "title": "Test",
            "module": "Test Module",
            "assessment_type": "Individual essay",
            "task_sections": [{"title": "Part 1", "description": "Do stuff"}],
            "rubric_criteria": [{"criterion": "Knowledge", "weight": "25 marks"}],
            "word_limit": "3,000 words",
        }
        draft = build_draft_starter(summary)
        assert "Rubric Self-Audit" in draft
        assert "Knowledge" in draft
        assert "Word count" in draft or "word count" in draft.lower()


# ── generate_for_brief validation ─────────────────────────────────────

class TestGenerateForBriefValidation:
    def test_missing_file_raises(self, tmp_path):
        fake = tmp_path / "nonexistent.docx"
        with pytest.raises(FileNotFoundError):
            generate_for_brief(fake, tmp_path)

    def test_wrong_extension_raises(self, tmp_path):
        fake = tmp_path / "brief.txt"
        fake.write_text("hello")
        with pytest.raises(ValueError, match="Expected a .docx or .pdf"):
            generate_for_brief(fake, tmp_path)


# ── infer_expected_output ─────────────────────────────────────────────

class TestInferExpectedOutput:
    def test_analysis(self):
        assert "Critical analysis" in infer_expected_output("CSR Strategy Analysis")

    def test_reflection(self):
        assert "reflection" in infer_expected_output("Personal Reflection").lower()

    def test_ethical(self):
        assert "ethical" in infer_expected_output("Ethical Issue Deep Dive").lower()

    def test_fallback(self):
        result = infer_expected_output("Unknown Topic")
        assert "brief" in result.lower()
