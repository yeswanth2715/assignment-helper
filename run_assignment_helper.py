from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from scripts.generate_workflow_artifacts import generate_for_brief

try:
    from scripts.llm_client import LLMConfig
except ImportError:
    LLMConfig = None  # type: ignore[assignment]

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = {".docx", ".pdf"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process every .docx/.pdf brief in the briefs folder and generate assignment helper artifacts."
    )
    parser.add_argument(
        "--briefs-dir",
        default="briefs",
        help="Directory containing one or more .docx or .pdf assignment briefs.",
    )
    parser.add_argument(
        "--output-dir",
        default="workflow_runs",
        help="Directory where generated artifact folders should be written.",
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        help="Use LLM to generate actual analysis, Harvard citations, tables, and figures "
             "(requires OPENROUTER_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY env var).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    briefs_dir = Path(args.briefs_dir)
    output_dir = Path(args.output_dir)

    if not briefs_dir.exists():
        logger.error("Brief directory not found: %s", briefs_dir)
        return 1

    briefs = sorted(
        f for f in briefs_dir.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not briefs:
        logger.error("No .docx or .pdf briefs found in: %s", briefs_dir)
        return 1

    # Configure LLM
    llm_config = None
    if args.llm:
        if LLMConfig is None:
            logger.error("LLM modules not available. Install openai / anthropic packages.")
            return 1
        llm_config = LLMConfig.from_env()
        if llm_config is None:
            logger.error(
                "--llm flag set but no API key found. "
                "Set OPENROUTER_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY."
            )
            return 1
        logger.info("LLM enabled via %s (model: %s)", llm_config.provider, llm_config.model)

    errors: list[str] = []
    for brief in briefs:
        try:
            target_dir = generate_for_brief(brief, output_dir, llm_config=llm_config)
            mode = "LLM draft" if llm_config else "placeholder template"
            logger.info("Generated %s for %s -> %s", mode, brief.name, target_dir)
        except Exception:
            logger.exception("Failed to process %s", brief.name)
            errors.append(brief.name)

    if errors:
        logger.warning("Finished with errors in: %s", ", ".join(errors))
    else:
        if llm_config:
            logger.info(
                "Done. The generated .docx contains a complete draft with analysis, "
                "citations, tables, and figures. Humanise the language before submission."
            )
        else:
            logger.info(
                "Done (placeholder mode). Review the template, fill in analysis, "
                "or re-run with --llm for AI-generated content."
            )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
