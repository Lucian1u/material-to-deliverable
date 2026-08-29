#!/usr/bin/env python3
"""Initialize a material-to-deliverable project without overwriting user files."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


WORKING_FILES = (
    "01_task-brief.md",
    "02_material-index.md",
    "03_gaps-and-conflicts.md",
    "04_source-backed-outline.md",
    "05_main-deliverable.md",
    "06_one-page-summary.md",
    "07_source-index.md",
    "08_audit-report.md",
)


class InitError(RuntimeError):
    """Raised when initialization would be unsafe or destructive."""


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def reject_unsafe_target(target: Path) -> None:
    resolved = target.resolve()
    if resolved == Path(resolved.anchor):
        raise InitError("Refusing to initialize a filesystem root.")
    if resolved == Path.home().resolve():
        raise InitError("Refusing to initialize the user home directory.")


def collision_paths(target: Path) -> list[Path]:
    collisions: list[Path] = []
    working = target / "01_working"
    delivery = target / "02_delivery"

    for name in WORKING_FILES:
        path = working / name
        if path.exists():
            collisions.append(path)

    if delivery.exists():
        collisions.extend(sorted(path for path in delivery.iterdir()))

    return collisions


def initialize_project(target: Path) -> list[Path]:
    target = target.expanduser().resolve()
    reject_unsafe_target(target)

    templates = skill_root() / "assets" / "project-templates"
    missing_templates = [name for name in WORKING_FILES if not (templates / name).is_file()]
    if missing_templates:
        joined = ", ".join(missing_templates)
        raise InitError(f"Skill templates are missing: {joined}")

    collisions = collision_paths(target)
    if collisions:
        rendered = "\n".join(f"- {path}" for path in collisions)
        raise InitError(
            "Refusing to overwrite an existing generated project. "
            "Resume the existing project or choose another directory:\n"
            f"{rendered}"
        )

    input_dir = target / "00_input"
    working_dir = target / "01_working"
    delivery_dir = target / "02_delivery"

    input_dir.mkdir(parents=True, exist_ok=True)
    working_dir.mkdir(parents=True, exist_ok=True)
    delivery_dir.mkdir(parents=True, exist_ok=True)

    created: list[Path] = [input_dir, working_dir, delivery_dir]
    for name in WORKING_FILES:
        destination = working_dir / name
        shutil.copyfile(templates / name, destination)
        created.append(destination)

    return created


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create 00_input, 01_working templates, and 02_delivery safely."
    )
    parser.add_argument("target", type=Path, help="Explicit project directory")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        created = initialize_project(args.target)
    except InitError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    print("Initialized material-to-deliverable project:")
    for path in created:
        print(f"- {path}")
    print("Place real source files in 00_input before running the skill workflow.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
