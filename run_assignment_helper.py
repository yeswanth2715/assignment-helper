from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from scripts.generate_workflow_artifacts import generate_for_brief

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

    errors: list[str] = []
    for brief in briefs:
        try:
            target_dir = generate_for_brief(brief, output_dir)
            logger.info("Generated helper package for %s -> %s", brief.name, target_dir)
        except Exception:
            logger.exception("Failed to process %s", brief.name)
            errors.append(brief.name)

    if errors:
        logger.warning("Finished with errors in: %s", ", ".join(errors))
    else:
        logger.info(
            "Done. Review the draft starter, figure plan, and checklist before writing the final submission."
        )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
