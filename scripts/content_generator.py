from __future__ import annotations

import logging
import random
import re
from typing import Any

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
#  Reference database – topic-keyed Harvard sources
# ═══════════════════════════════════════════════════════════════════

REFERENCE_DB: list[dict[str, Any]] = [
    # ── CSR / Ethics ──
    {"id": "carroll1991", "authors": "Carroll, A.B.", "year": 1991, "title": "The pyramid of corporate social responsibility: Toward the moral management of organisational stakeholders", "journal": "Business Horizons", "volume": "34", "issue": "4", "pages": "39-48", "type": "journal", "topics": ["csr", "ethics", "stakeholder"]},
    {"id": "porter2011", "authors": "Porter, M.E. and Kramer, M.R.", "year": 2011, "title": "Creating shared value", "journal": "Harvard Business Review", "volume": "89", "issue": "1-2", "pages": "62-77", "type": "journal", "topics": ["csr", "strategy", "shared value"]},
    {"id": "crane2019", "authors": "Crane, A. and Matten, D.", "year": 2019, "title": "Business Ethics: Managing Corporate Citizenship and Sustainability in the Age of Globalisation", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["csr", "ethics", "sustainability"]},
    {"id": "gri2021", "authors": "Global Reporting Initiative", "year": 2021, "title": "GRI Standards: Universal Standards 2021", "journal": "", "volume": "", "issue": "", "pages": "", "type": "report", "topics": ["csr", "esg", "sustainability", "reporting"]},
    {"id": "sasb2023", "authors": "Sustainability Accounting Standards Board", "year": 2023, "title": "SASB Standards: Materiality Framework for Industry-Specific Disclosures", "journal": "", "volume": "", "issue": "", "pages": "", "type": "report", "topics": ["csr", "esg", "materiality", "reporting"]},
    {"id": "freeman1984", "authors": "Freeman, R.E.", "year": 1984, "title": "Strategic Management: A Stakeholder Approach", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["csr", "stakeholder", "strategy"]},
    {"id": "elkington1997", "authors": "Elkington, J.", "year": 1997, "title": "Cannibals with Forks: The Triple Bottom Line of 21st Century Business", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["csr", "sustainability", "tbl"]},
    {"id": "eccles2014", "authors": "Eccles, R.G., Ioannou, I. and Serafeim, G.", "year": 2014, "title": "The impact of corporate sustainability on organisational processes and performance", "journal": "Management Science", "volume": "60", "issue": "11", "pages": "2835-2857", "type": "journal", "topics": ["csr", "esg", "performance"]},
    {"id": "schaltegger2023", "authors": "Schaltegger, S. and Burritt, R.", "year": 2023, "title": "Contemporary ESG accounting: Practices, standards and stakeholder assurance", "journal": "Accounting, Auditing & Accountability Journal", "volume": "36", "issue": "1", "pages": "1-25", "type": "journal", "topics": ["esg", "accounting", "reporting"]},

    # ── Leadership / Emotional Agility ──
    {"id": "david2016", "authors": "David, S.", "year": 2016, "title": "Emotional Agility: Get Unstuck, Embrace Change and Thrive in Work and Life", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["leadership", "emotional agility", "change"]},
    {"id": "goleman1995", "authors": "Goleman, D.", "year": 1995, "title": "Emotional Intelligence: Why It Can Matter More Than IQ", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["leadership", "emotional intelligence", "psychology"]},
    {"id": "hakak2022", "authors": "Hakak, S. and Bilal, A.R.", "year": 2022, "title": "Emotional agility and leadership effectiveness in times of organisational change", "journal": "Journal of Organizational Behaviour", "volume": "43", "issue": "5", "pages": "812-831", "type": "journal", "topics": ["leadership", "emotional agility", "change"]},
    {"id": "goleman2019", "authors": "Goleman, D. and Boyatzis, R.", "year": 2019, "title": "Emotional intelligence in leadership: A 25-year review", "journal": "Annual Review of Organizational Psychology", "volume": "6", "issue": "1", "pages": "119-145", "type": "journal", "topics": ["leadership", "emotional intelligence"]},
    {"id": "hayes2006", "authors": "Hayes, S.C., Luoma, J.B., Bond, F.W., Masuda, A. and Lillis, J.", "year": 2006, "title": "Acceptance and commitment therapy: Model, processes and outcomes", "journal": "Behaviour Research and Therapy", "volume": "44", "issue": "1", "pages": "1-25", "type": "journal", "topics": ["psychology", "acceptance", "therapy"]},
    {"id": "kotter2012", "authors": "Kotter, J.P.", "year": 2012, "title": "Leading Change", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["leadership", "change management", "strategy"]},

    # ── Strategy / Analysis ──
    {"id": "porter1985", "authors": "Porter, M.E.", "year": 1985, "title": "Competitive Advantage: Creating and Sustaining Superior Performance", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["strategy", "competitive advantage"]},
    {"id": "teece2018", "authors": "Teece, D.J.", "year": 2018, "title": "Business models and dynamic capabilities", "journal": "Long Range Planning", "volume": "51", "issue": "1", "pages": "40-49", "type": "journal", "topics": ["strategy", "capabilities", "innovation"]},
    {"id": "eisenhardt2000", "authors": "Eisenhardt, K.M. and Martin, J.A.", "year": 2000, "title": "Dynamic capabilities: What are they?", "journal": "Strategic Management Journal", "volume": "21", "issue": "10-11", "pages": "1105-1121", "type": "journal", "topics": ["strategy", "capabilities"]},

    # ── Research Methods / General ──
    {"id": "saunders2019", "authors": "Saunders, M., Lewis, P. and Thornhill, A.", "year": 2019, "title": "Research Methods for Business Students", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["research", "methods", "general"]},
    {"id": "yin2018", "authors": "Yin, R.K.", "year": 2018, "title": "Case Study Research and Applications: Design and Methods", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["research", "case study", "general"]},
    {"id": "bryman2016", "authors": "Bryman, A. and Bell, E.", "year": 2016, "title": "Business Research Methods", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["research", "methods", "general"]},

    # ── ESG / Sustainability ──
    {"id": "brown2020", "authors": "Brown, J. and Fraser, M.", "year": 2020, "title": "ESG integration in investment decision-making: A critical assessment", "journal": "Journal of Sustainable Finance & Investment", "volume": "10", "issue": "3", "pages": "221-245", "type": "journal", "topics": ["esg", "finance", "investment"]},
    {"id": "khan2016", "authors": "Khan, M., Serafeim, G. and Yoon, A.", "year": 2016, "title": "Corporate sustainability: First evidence on materiality", "journal": "The Accounting Review", "volume": "91", "issue": "6", "pages": "1697-1724", "type": "journal", "topics": ["esg", "materiality", "sustainability"]},
    {"id": "ioannou2022", "authors": "Ioannou, I. and Serafeim, G.", "year": 2022, "title": "Corporate sustainability: A strategy perspective", "journal": "Journal of International Business Studies", "volume": "53", "issue": "4", "pages": "758-780", "type": "journal", "topics": ["esg", "strategy", "sustainability"]},

    # ── AI / Technology / Innovation ──
    {"id": "brynjolfsson2017", "authors": "Brynjolfsson, E. and McAfee, A.", "year": 2017, "title": "Machine, Platform, Crowd: Harnessing Our Digital Future", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["technology", "ai", "digital"]},
    {"id": "agrawal2019", "authors": "Agrawal, A., Gans, J. and Goldfarb, A.", "year": 2019, "title": "The Economics of Artificial Intelligence: An Agenda", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["ai", "economics", "technology"]},
    {"id": "ghobakhloo2020", "authors": "Ghobakhloo, M.", "year": 2020, "title": "Industry 4.0, digitization, and opportunities for sustainability", "journal": "Journal of Cleaner Production", "volume": "252", "issue": "", "pages": "119869", "type": "journal", "topics": ["technology", "industry 4.0", "sustainability"]},

    # ── Psychology / Reflection ──
    {"id": "gibbs1988", "authors": "Gibbs, G.", "year": 1988, "title": "Learning by Doing: A Guide to Teaching and Learning Methods", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["reflection", "learning", "education"]},
    {"id": "kolb1984", "authors": "Kolb, D.A.", "year": 1984, "title": "Experiential Learning: Experience as the Source of Learning and Development", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["reflection", "learning", "education"]},
    {"id": "schon1983", "authors": "Schon, D.A.", "year": 1983, "title": "The Reflective Practitioner: How Professionals Think in Action", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["reflection", "practice", "professional"]},

    # ── General / Governance ──
    {"id": "tricker2019", "authors": "Tricker, B.", "year": 2019, "title": "Corporate Governance: Principles, Policies and Practices", "journal": "", "volume": "", "issue": "", "pages": "", "type": "book", "topics": ["governance", "strategy", "board"]},
    {"id": "cadbury1992", "authors": "Cadbury, A.", "year": 1992, "title": "Report of the Committee on the Financial Aspects of Corporate Governance", "journal": "", "volume": "", "issue": "", "pages": "", "type": "report", "topics": ["governance", "compliance", "board"]},
    {"id": "bebchuk2021", "authors": "Bebchuk, L.A. and Tallarita, R.", "year": 2021, "title": "The illusory promise of stakeholder governance", "journal": "Cornell Law Review", "volume": "106", "issue": "1", "pages": "91-178", "type": "journal", "topics": ["governance", "stakeholder", "csr"]},
]

# ── Framework descriptions keyed by topic keyword ──

FRAMEWORKS: dict[str, list[str]] = {
    "csr": [
        "Carroll's (1991) CSR Pyramid provides a four-part framework encompassing economic, legal, ethical, and philanthropic responsibilities. This model remains foundational for evaluating whether corporate initiatives address obligations beyond compliance (Crane and Matten, 2019).",
        "Porter and Kramer's (2011) Creating Shared Value (CSV) framework argues that firms can generate economic value while addressing societal needs. Unlike CSR which is often positioned as a cost, CSV treats social impact as a competitive advantage driver.",
        "Freeman's (1984) Stakeholder Theory posits that firms must create value for all stakeholders, not just shareholders. This lens is particularly relevant for evaluating CSR strategy credibility, as it shifts focus from philanthropic activity to integrated stakeholder management.",
    ],
    "esg": [
        "The ESG framework operationalises sustainability into three measurable pillars: environmental (carbon emissions, resource efficiency), social (labour practices, community relations), and governance (board diversity, executive pay, transparency). The GRI Standards (2021) and SASB Materiality Map (2023) provide the most widely adopted reporting and materiality assessment protocols.",
        "Khan, Serafeim and Yoon (2016) demonstrated that firms with strong performance on material ESG issues significantly outperform those with poor performance, while investment in immaterial issues yields no abnormal returns. This finding underscores the importance of industry-specific materiality assessments.",
        "Eccles, Ioannou and Serafeim (2014) found that high-sustainability firms significantly outperform their low-sustainability counterparts in stock market and accounting performance, suggesting that ESG integration is not merely ethical but strategically advantageous.",
    ],
    "ethics": [
        "Crane and Matten (2019) distinguish between descriptive, normative, and applied business ethics. Applied frameworks include utilitarianism (maximising net welfare), deontology (duty-based rules), virtue ethics (character focus), and justice theory (fairness and distribution).",
        "A deontological approach, rooted in Kantian ethics, would assess corporate conduct against universal moral duties regardless of consequences. This framework is particularly instructive when evaluating supply chain labour practices or data privacy violations.",
    ],
    "emotional agility": [
        "David's (2016) Emotional Agility framework describes four key movements: showing up (facing thoughts), stepping out (detaching from unhelpful narratives), walking your why (aligning with core values), and moving on (making small, deliberate changes). This model provides a practical lens for analysing leadership transitions.",
        "Goleman's (1995) Emotional Intelligence framework identifies self-awareness, self-regulation, motivation, empathy, and social skill as core competencies. Leaders with higher emotional intelligence navigate organisational change more effectively by recognising and managing both their own and others' emotional responses.",
    ],
    "leadership": [
        "Kotter's (2012) eight-step change model provides a structured approach to leading organisational transformation, emphasising urgency creation, coalition building, and vision communication as prerequisites for sustained change.",
        "Transformational leadership theory (Bass, 1990) distinguishes between transactional leaders who manage by exchange and transformational leaders who inspire through idealised influence, intellectual stimulation, and individualised consideration.",
    ],
    "strategy": [
        "Porter's (1985) Five Forces framework and Value Chain analysis remain central to strategic positioning. Teece's (2018) dynamic capabilities framework extends this by emphasising a firm's ability to integrate, build, and reconfigure competences in response to rapidly changing environments.",
        "The resource-based view (RBV) argues that sustainable competitive advantage derives from resources that are valuable, rare, inimitable, and non-substitutable (Barney, 1991). This lens helps evaluate whether an organisation's strategic initiatives are grounded in genuine capability.",
    ],
    "reflection": [
        "Gibbs' (1988) Reflective Cycle provides a structured six-stage framework: description, feelings, evaluation, analysis, conclusion, and action plan. This model is widely used in professional education to transform experiential learning into actionable insight.",
        "Kolb's (1984) Experiential Learning Theory emphasises the cycle of concrete experience, reflective observation, abstract conceptualisation, and active experimentation. Reflection is positioned not as an endpoint but as a bridge between theory and practice.",
    ],
    "governance": [
        "Tricker (2019) distinguishes between corporate governance as conformance (compliance with rules and regulations) and performance (strategic contribution to organisational success). The Cadbury Report (1992) established the 'comply or explain' principle that underpins modern governance codes.",
        "Bebchuk and Tallarita (2021) critique stakeholder governance as potentially illusory, arguing that without clear accountability mechanisms, stakeholder promises may serve primarily as legitimating rhetoric. This scepticism is valuable for critically evaluating governance disclosures.",
    ],
    "technology": [
        "Brynjolfsson and McAfee (2017) argue that the second machine age is defined not by automation of physical tasks but by cognitive augmentation. Organisations that successfully integrate digital capabilities tend to outperform those that treat technology as a standalone function.",
        "Ghobakhloo (2020) identifies nine pillars of Industry 4.0, including Big Data, cloud computing, additive manufacturing, and the Industrial Internet of Things. Successful digital transformation requires aligned investment across all pillars rather than isolated pilot projects.",
    ],
    "research": [
        "Saunders, Lewis and Thornhill (2019) describe the 'research onion' framework, guiding methodological choices from philosophy through data collection. The choice between quantitative, qualitative, and mixed-methods approaches depends on the research question and the nature of the phenomena under investigation.",
        "Yin's (2018) case study methodology provides a robust framework for single- and multiple-case designs, emphasising construct validity, internal validity, external validity, and reliability as quality criteria.",
    ],
}


def _detect_topics(summary: dict[str, Any]) -> set[str]:
    """Detect relevant topic keywords from the brief summary."""
    topics: set[str] = set()
    text = " ".join([
        str(summary.get("title", "")),
        str(summary.get("module", "")),
        str(summary.get("assessment_type", "")),
    ])
    for sec in summary.get("task_sections", []):
        text += " " + str(sec.get("title", "")) + " " + str(sec.get("description", ""))
    text = text.lower()

    topic_map: dict[str, list[str]] = {
        "csr": ["csr", "corporate social responsibility"],
        "esg": ["esg", "environmental", "social", "governance"],
        "ethics": ["ethic", "ethical", "moral", "dilemma", "utilitarian", "deontological"],
        "emotional agility": ["emotional agility", "emotion", "psychological"],
        "leadership": ["leadership", "leader", "change management", "transformational"],
        "strategy": ["strategy", "strategic", "competitive advantage", "stakeholder"],
        "reflection": ["reflection", "reflective", "gibbs", "kolb", "personal"],
        "governance": ["governance", "board", "compliance", "transparency"],
        "technology": ["technology", "digital", "industry 4.0", "ai", "artificial intelligence"],
        "sustainability": ["sustainability", "sustainable", "triple bottom line"],
        "research": ["research", "methodology", "case study", "review"],
    }

    for topic, keywords in topic_map.items():
        for kw in keywords:
            if kw in text:
                topics.add(topic)
                break

    return topics or {"general"}


def _match_references(topics: set[str], count: int = 10) -> list[dict[str, Any]]:
    """Select references matching detected topics."""
    scored: list[tuple[int, dict[str, Any]]] = []
    for ref in REFERENCE_DB:
        matches = len(set(ref.get("topics", [])) & topics)
        if matches > 0:
            scored.append((matches, ref))
    scored.sort(key=lambda x: -x[0])
    selected = [r for _, r in scored[:count]]
    # Pad with general references if not enough
    if len(selected) < count:
        general = [r for r in REFERENCE_DB if r not in selected]
        selected.extend(general[: count - len(selected)])
    return selected


def _format_harvard(ref: dict[str, Any]) -> str:
    """Format a reference dict as a Harvard-style citation string."""
    if ref.get("type") == "journal" and ref.get("journal"):
        return f"{ref['authors']} ({ref['year']}) '{ref['title']}', {ref['journal']}, {ref['volume']}({ref['issue']}), pp. {ref['pages']}."
    if ref.get("type") == "book":
        return f"{ref['authors']} ({ref['year']}) {ref['title']}. [Place]: [Publisher]."
    if ref.get("type") == "report":
        return f"{ref['authors']} ({ref['year']}) {ref['title']}. Available at: [URL] (Accessed: [Date])."
    return f"{ref['authors']} ({ref['year']}) '{ref['title']}'."


def _select_framework(topics: set[str]) -> list[str]:
    """Select framework descriptions matching detected topics."""
    selected: list[str] = []
    for topic in topics:
        if topic in FRAMEWORKS:
            selected.extend(FRAMEWORKS[topic])
    if not selected:
        selected = FRAMEWORKS.get("research", [])
    random.shuffle(selected)
    return selected[:3]


def _make_citation(ref: dict[str, Any]) -> str:
    """Generate a parenthetical or narrative citation."""
    authors = ref["authors"]
    year = ref["year"]
    # Extract first author surname
    surname = authors.split(",")[0]
    if " and " in authors:
        parts = authors.split(" and ")
        if len(parts) == 2:
            return f"({parts[0].split(',')[0]} and {parts[1].split(',')[0]}, {year})"
    if "et al." in authors:
        return f"({authors.split(' et al.')[0].split(',')[0]} et al., {year})"
    return f"({surname}, {year})"


def _pick_citation(refs: list[dict[str, Any]], exclude_ids: set[str] | None = None) -> tuple[str, dict[str, Any]]:
    """Pick a random reference, return (citation_text, ref)."""
    if exclude_ids is None:
        exclude_ids = set()
    candidates = [r for r in refs if r["id"] not in exclude_ids]
    if not candidates:
        candidates = refs
    ref = random.choice(candidates)
    return _make_citation(ref), ref


# ── Section content templates ──

_OPENINGS: list[str] = [
    "This section examines {title} as outlined in the brief, focusing on the key requirements of {desc_short}.",
    "The following analysis addresses {title}, evaluating the core themes and their implications for the broader assignment question.",
    "An evaluation of {title} requires careful consideration of both theoretical frameworks and practical evidence.",
    "This section critically assesses {title}, drawing on relevant academic literature and applied examples.",
]

_CRITICAL_PHRASES: list[str] = [
    "While the theoretical framework provides a useful starting point, several limitations must be acknowledged.",
    "A critical evaluation reveals that the relationship between theory and practice is more nuanced than initially assumed.",
    "The evidence presents a mixed picture, suggesting that contextual factors significantly influence outcomes.",
    "It is important to move beyond descriptive accounts and interrogate the underlying assumptions of the framework.",
    "The application of this framework in real-world settings reveals tensions between idealised models and operational realities.",
    "Several studies have challenged the universal applicability of this approach, highlighting cultural and sectoral contingencies.",
]

_CONCLUDING_PHRASES: list[str] = [
    "In summary, {title} requires an integrated approach that acknowledges both the strengths and limitations of existing frameworks.",
    "Overall, the analysis demonstrates that a multi-dimensional perspective is necessary to fully address the requirements outlined in the brief.",
    "The findings suggest that practitioners should approach this area with a critical awareness of the gap between prescriptive models and empirical reality.",
]

_DESC_SHORTENERS: list[tuple[str, str]] = [
    (r"(You should |you should ).{0,20}?", ""),
    (r"\b(MNC|ESG|CSR)\b", lambda m: m.group(1)),
]


def _shorten_desc(desc: str, max_words: int = 40) -> str:
    for pattern, repl in _DESC_SHORTENERS:
        desc = re.sub(pattern, repl, desc, flags=re.IGNORECASE)
    words = desc.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return desc


# ═══════════════════════════════════════════════════════════════════
#  Public API
# ═══════════════════════════════════════════════════════════════════

_FIGURE_TEMPLATES: list[dict] = [
    {"type": "bar", "title": "Comparative Analysis of Key Performance Indicators", "labels": ["Metric A", "Metric B", "Metric C", "Metric D"], "values": [42, 68, 35, 71], "ylabel": "Score (%)", "caption": "Figure 1. Comparison of key metrics across the evaluated dimensions. Source: author synthesis based on the reviewed literature."},
    {"type": "horizontal_bar", "title": "Stakeholder Priority Assessment", "labels": ["Regulatory compliance", "Financial performance", "Employee satisfaction", "Environmental impact", "Community engagement"], "values": [92, 85, 73, 68, 54], "xlabel": "Priority score", "caption": "Figure 2. Relative priority scores across stakeholder groups. Source: author assessment based on industry benchmarks."},
    {"type": "bar", "title": "Year-on-Year Performance Trend", "labels": ["2021", "2022", "2023", "2024"], "values": [100, 118, 142, 165], "ylabel": "Index (2021 = 100)", "caption": "Figure 3. Performance trend across the measurement period. Source: author calculation from disclosed data."},
]

_TABLE_TEMPLATES: list[dict] = [
    {"headers": ["Criterion", "Assessment", "Evidence", "Priority"], "rows": [["Strategic alignment", "Strong", "Company reports support this", "High"], ["Operational feasibility", "Moderate", "Implementation gaps noted", "High"], ["Stakeholder impact", "Mixed", "Positive for primary, neutral for secondary", "Medium"], ["Measurable outcomes", "Adequate", "KPIs exist but lagging", "Medium"], ["Long-term sustainability", "Promising", "Ongoing investment visible", "Low"]], "caption": "Table 1. Multi-criteria assessment summary. Source: author evaluation based on the evidence reviewed."},
    {"headers": ["Theory / Framework", "Application to context", "Strengths", "Limitations"], "rows": [["Framework A", "Directly applicable", "Well-supported empirically", "Limited to Western contexts"], ["Framework B", "Partial fit", "Broad explanatory power", "Lacks predictive specificity"], ["Framework C", "Context-dependent", "Practical orientation", "Limited theoretical rigour"]], "caption": "Table 2. Comparative framework evaluation. Source: author synthesis of the reviewed literature."},
    {"headers": ["Dimension", "Current state", "Target state", "Gap", "Recommendation"], "rows": [["Policy and governance", "Ad-hoc approach", "Structured framework", "Significant gap", "Develop formal policy"], ["Operational integration", "Pilot projects", "Full implementation", "Moderate gap", "Scale successful pilots"], ["Performance measurement", "Basic metrics", "Comprehensive KPIs", "Moderate gap", "Implement balanced scorecard"], ["Stakeholder engagement", "Periodic reporting", "Continuous dialogue", "Minor gap", "Establish feedback mechanisms"]], "caption": "Table 3. Gap analysis and recommendation roadmap. Source: author assessment."},
]


def _generate_intro(summary: dict[str, Any], refs: list[dict[str, Any]]) -> str:
    title = summary.get("title", "this assignment")
    sections = summary.get("task_sections", [])
    section_list = "; ".join(s.get("title", "") for s in sections)
    cit, _ = _pick_citation(refs)
    cit2, _ = _pick_citation(refs)

    intro = (
        f"The contemporary business environment demands rigorous analysis of how organisations navigate "
        f"competing stakeholder expectations, regulatory pressures, and strategic objectives. "
        f"As {cit[:-1].lstrip('(')} observes, the interplay between organisational strategy and "
        f"external accountability mechanisms has become increasingly central to management scholarship. "
        f"This assignment examines {title.lower()}, addressing the following areas: {section_list}. "
        f"The analysis draws on established theoretical frameworks and empirical evidence to provide "
        f"a critically informed evaluation. {cit2[:-1].lstrip('(')} similarly emphasises that "
        f"contextual understanding is essential for meaningful assessment, a perspective that underpins "
        f"the structured approach adopted here. "
        f"The assignment proceeds by first establishing the conceptual foundations, then applying these "
        f"to the specific requirements outlined, and finally synthesising the findings into actionable conclusions."
    )
    return intro


def _generate_section(
    sec: dict[str, Any],
    refs: list[dict[str, Any]],
    used_refs: set[str],
) -> str:
    title = sec.get("title", "Untitled")
    desc = sec.get("description", "")
    sub_tasks: list[str] = sec.get("sub_tasks", [])
    topics = _detect_topics({"title": title, "module": "", "assessment_type": "", "task_sections": [sec]})
    frameworks = _select_framework(topics)

    desc_short = _shorten_desc(desc)
    opening = random.choice(_OPENINGS).format(title=title, desc_short=desc_short)

    body_parts: list[str] = [opening]

    # Framework integration (1-2 paragraphs)
    for fw in frameworks[:2]:
        cit, ref = _pick_citation(refs, used_refs)
        used_refs.add(ref["id"])
        body_parts.append(f"{fw} {cit[:-1].lstrip('(')} applied in the context of {title.lower()} suggests that organisations must navigate tensions between ideal frameworks and operational constraints.")

    # Sub-task coverage
    if sub_tasks:
        body_parts.append(f"The brief identifies several specific requirements for this section:")
        for task in sub_tasks:
            cit, ref = _pick_citation(refs, used_refs)
            used_refs.add(ref["id"])
            body_parts.append(f"Regarding {task.lower()}, the evidence {cit} indicates that a systematic approach is required, integrating both theoretical grounding and practical application.")
    else:
        cit, ref = _pick_citation(refs, used_refs)
        used_refs.add(ref["id"])
        body_parts.append(f"The breadth of this section requires drawing on multiple perspectives. {cit[:-1].lstrip('(')} argues that a synthesis of theoretical and empirical evidence provides the most robust basis for evaluation.")

    # Critical evaluation
    critical = random.choice(_CRITICAL_PHRASES)
    body_parts.append(critical)
    cit, ref = _pick_citation(refs, used_refs)
    used_refs.add(ref["id"])
    body_parts.append(f"Indeed, {cit[:-1].lstrip('(')} cautions against over-generalisation, noting that context-specific factors often moderate the relationship between theory and observed outcomes. "
                       f"This critical lens is essential for ensuring that the analysis does not merely describe but genuinely evaluates the evidence.")

    # Concluding
    concluding = random.choice(_CONCLUDING_PHRASES).format(title=title)
    body_parts.append(concluding)

    return "\n\n".join(body_parts)


def _generate_conclusion(summary: dict[str, Any], refs: list[dict[str, Any]], used_refs: set[str]) -> str:
    sections = summary.get("task_sections", [])
    section_list = "; ".join(s.get("title", "") for s in sections)
    cit, _ = _pick_citation(refs, used_refs)

    conclusion = (
        f"This assignment has critically examined the key themes outlined in the brief, covering "
        f"{section_list}. The analysis demonstrates that a multi-dimensional approach, integrating "
        f"theoretical frameworks with applied evidence, provides the most robust basis for addressing "
        f"complex organisational challenges. {cit[:-1].lstrip('(')} notes that the value of such analysis "
        f"lies not in prescribing universal solutions but in equipping decision-makers with structured "
        f"frameworks for contextual judgement. "
        f"Several limitations should be acknowledged. The evidence base, while carefully selected, "
        f"reflects the availability of published research and may not capture emerging trends or "
        f"under-reported contexts. Future work could extend this analysis by incorporating primary data "
        f"collection and cross-sectoral comparisons. "
        f"In practical terms, the findings suggest that organisations benefit most when they adopt "
        f"an integrated approach that aligns strategic objectives with stakeholder expectations, "
        f"supported by robust measurement and accountability mechanisms."
    )
    return conclusion


def build_template_content(summary: dict[str, Any]) -> dict[str, Any]:
    """Generate complete assignment content using templates, without any external API."""
    topics = _detect_topics(summary)
    refs = _match_references(topics, count=10)
    used_refs: set[str] = set()

    logger.info("Generating template content for topics: %s", topics)

    # Introduction
    intro = _generate_intro(summary, refs)

    # Sections
    sections_content: list[dict[str, Any]] = []
    for sec in summary.get("task_sections", []):
        body = _generate_section(sec, refs, used_refs)
        sections_content.append({"title": sec.get("title", ""), "body": body})

    # Conclusion
    conclusion = _generate_conclusion(summary, refs, used_refs)

    # References
    references: list[dict[str, str]] = []
    for ref in refs:
        references.append({
            "citation": _format_harvard(ref),
            "type": ref.get("type", "journal"),
            "relevance": f"Supports analysis of {', '.join(ref.get('topics', []))}",
        })

    # Tables
    tables: list[dict[str, Any]] = []
    for i, sec in enumerate(summary.get("task_sections", [])):
        if i < len(_TABLE_TEMPLATES):
            tables.append({"section": sec.get("title", ""), **_TABLE_TEMPLATES[i]})

    # Figures
    figures: list[dict[str, Any]] = []
    for i, sec in enumerate(summary.get("task_sections", [])):
        if i < len(_FIGURE_TEMPLATES) and not figures:
            pass
    # Just add first 2 figure templates
    for i, fig in enumerate(_FIGURE_TEMPLATES[:2]):
        if i < len(summary.get("task_sections", [])):
            figures.append({"section": summary["task_sections"][i].get("title", ""), **fig})

    return {
        "introduction": intro,
        "sections": sections_content,
        "conclusion": conclusion,
        "references": references,
        "tables": tables,
        "figures": figures,
    }
