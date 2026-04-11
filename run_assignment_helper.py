from __future__ import annotations

import argparse
import sys
from pathlib import Path

from scripts.generate_workflow_artifacts import generate_for_brief


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process every .docx brief in the briefs folder and generate assignment helper artifacts."
    )
    parser.add_argument(
        "--briefs-dir",
        default="briefs",
        help="Directory containing one or more .docx assignment briefs.",
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
        print(f"Brief directory not found: {briefs_dir}")
        return 1

    briefs = sorted(briefs_dir.glob("*.docx"))
    if not briefs:
        print(f"No .docx briefs found in: {briefs_dir}")
        return 1

    for brief in briefs:
        target_dir = generate_for_brief(brief, output_dir)
        print(f"Generated helper package for {brief.name} -> {target_dir}")

    print("Done. Review the draft starter, figure plan, and checklist before writing the final submission.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
