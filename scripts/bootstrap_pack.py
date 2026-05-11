#!/usr/bin/env python3
"""
Copy the faceless content execution-pack templates into a target directory.

Usage:
    python bootstrap_pack.py --target /path/to/output [--mode service|media|hybrid|all]
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


VALID_MODES = {"service", "media", "hybrid", "all"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold the faceless-content execution pack.")
    parser.add_argument("--target", required=True, help="Directory to write the execution pack into.")
    parser.add_argument(
        "--mode",
        default="all",
        choices=sorted(VALID_MODES),
        help="Template subset to copy.",
    )
    return parser.parse_args()


def should_copy(name: str, mode: str) -> bool:
    if mode == "all":
        return True
    if name.startswith("shared-"):
        return True
    return name.startswith(f"{mode}-")


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    templates = root / "assets" / "templates"
    examples = root / "assets" / "examples"
    target = Path(args.target).resolve()

    target.mkdir(parents=True, exist_ok=True)
    (target / "templates").mkdir(exist_ok=True)
    (target / "examples").mkdir(exist_ok=True)

    copied = []

    for src_dir, dest_name in [(templates, "templates"), (examples, "examples")]:
        for src in sorted(src_dir.iterdir()):
            if src.is_dir():
                continue
            if not should_copy(src.name, args.mode):
                continue
            dest = target / dest_name / src.name
            shutil.copy2(src, dest)
            copied.append(dest)

    print(f"Copied {len(copied)} files to {target}")
    for path in copied:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
