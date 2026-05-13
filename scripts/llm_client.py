from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from typing import ClassVar, Literal

logger = logging.getLogger(__name__)


@dataclass
class LLMConfig:
    provider: Literal["openai", "anthropic", "openrouter"] = "openrouter"
    api_key: str = ""
    model: str = ""
    base_url: str = ""
    temperature: float = 0.7
    max_tokens: int = 4096

    PROVIDER_DEFAULTS: ClassVar[dict] = {
        "openai": {
            "model": "gpt-4o",
            "base_url": "https://api.openai.com/v1",
            "env_key": "OPENAI_API_KEY",
        },
        "anthropic": {
            "model": "claude-sonnet-4-20250514",
            "base_url": "https://api.anthropic.com/v1",
            "env_key": "ANTHROPIC_API_KEY",
        },
        "openrouter": {
            "model": "openai/gpt-4o",
            "base_url": "https://openrouter.ai/api/v1",
            "env_key": "OPENROUTER_API_KEY",
        },
    }

    @classmethod
    def from_env(cls) -> LLMConfig | None:
        for provider in ("openrouter", "openai", "anthropic"):
            defaults = cls.PROVIDER_DEFAULTS[provider]
            api_key = os.environ.get(defaults["env_key"]) or os.environ.get("LLM_API_KEY")
            if api_key:
                model = os.environ.get("LLM_MODEL", defaults["model"])
                base_url = os.environ.get("LLM_BASE_URL", defaults["base_url"])
                return cls(provider=provider, api_key=api_key, model=model, base_url=base_url)
        return None


def _system_prompt(summary: dict) -> str:
    rubric_str = "\n".join(
        f"- {c['criterion']} ({c['weight']})"
        for c in summary.get("rubric_criteria", [])
    )
    lo_str = "\n".join(f"- {lo}" for lo in summary.get("learning_outcomes", []))
    return f"""You are an academic assignment co-pilot writing a master's-level assignment draft.

Module: {summary.get('module', 'N/A')}
Assessment type: {summary.get('assessment_type', 'N/A')}
Word limit: {summary.get('word_limit', 'N/A')}

Rubric criteria:
{rubric_str or '- None detected'}

Learning outcomes:
{lo_str or '- None detected'}

Write in formal academic English. Use Harvard-style in-text citations throughout (Author, Year). Integrate theory and evidence critically (not just description). Include quantitative examples and data where appropriate. Every factual claim must have a plausible citation.

The student will later humanise the language to avoid AI detection flags, so write natural, varied prose — avoid repetitive sentence structures and formulaic transitions."""


def generate(prompt: str, summary: dict, config: LLMConfig | None = None) -> str:
    if config is None:
        config = LLMConfig.from_env()
    if config is None:
        raise RuntimeError(
            "No LLM API key found. Set OPENROUTER_API_KEY, OPENAI_API_KEY, "
            "ANTHROPIC_API_KEY, or LLM_API_KEY environment variable."
        )

    if config.provider == "anthropic":
        return _generate_anthropic(prompt, summary, config)
    return _generate_openai_compat(prompt, summary, config)


def _generate_openai_compat(prompt: str, summary: dict, config: LLMConfig) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=config.api_key, base_url=config.base_url)
    response = client.chat.completions.create(
        model=config.model,
        messages=[
            {"role": "system", "content": _system_prompt(summary)},
            {"role": "user", "content": prompt},
        ],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    return response.choices[0].message.content or ""


def _generate_anthropic(prompt: str, summary: dict, config: LLMConfig) -> str:
    from anthropic import Anthropic

    client = Anthropic(api_key=config.api_key)
    response = client.messages.create(
        model=config.model,
        system=_system_prompt(summary),
        messages=[{"role": "user", "content": prompt}],
        temperature=config.temperature,
        max_tokens=config.max_tokens,
    )
    return response.content[0].text if response.content else ""
