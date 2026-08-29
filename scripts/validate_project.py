#!/usr/bin/env python3
"""Validate project structure and obvious packaging mistakes.

This validator does not judge whether claims are true or adequately supported.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
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

DELIVERY_FILES = (
    "main-deliverable.md",
    "one-page-summary.md",
    "source-index.md",
    "readme.md",
)

PLACEHOLDER_PATTERN = re.compile(r"\{\{[^{}]+\}\}")
ABSOLUTE_PATH_PATTERNS = (
    re.compile(r"/Users/[^\s)]+"),
    re.compile(r"/home/[^\s)]+"),
    re.compile(r"[A-Za-z]:\\Users\\[^\s)]+"),
)
PROHIBITED_NAME_PARTS = (
    "raw",
    "unredacted",
    "draft",
    "chat",
    "prompt",
    "internal",
    "tmp",
    "原始",
    "未脱敏",
    "草稿",
    "聊天",
    "提示词",
    "内部",
    "临时",
)


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path, result: ValidationResult) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        result.errors.append(f"Expected UTF-8 Markdown but could not read: {path}")
        return ""


def check_required_paths(root: Path, stage: str, result: ValidationResult) -> None:
    required_dirs = (root / "00_input", root / "01_working", root / "02_delivery")
    for path in required_dirs:
        if not path.is_dir():
            result.errors.append(f"Missing required directory: {path}")

    for name in WORKING_FILES:
        path = root / "01_working" / name
        if not path.is_file():
            result.errors.append(f"Missing required working file: {path}")

    if stage == "delivery":
        for name in DELIVERY_FILES:
            path = root / "02_delivery" / name
            if not path.is_file():
                result.errors.append(f"Missing required delivery file: {path}")


def check_unresolved_placeholders(root: Path, result: ValidationResult) -> None:
    paths = [root / "01_working" / name for name in WORKING_FILES]
    paths.extend(root / "02_delivery" / name for name in DELIVERY_FILES)

    for path in paths:
        if not path.is_file():
            continue
        text = read_text(path, result)
        matches = sorted(set(PLACEHOLDER_PATTERN.findall(text)))
        if matches:
            preview = ", ".join(matches[:5])
            result.errors.append(f"Unresolved placeholders in {path}: {preview}")


def check_delivery_contents(root: Path, result: ValidationResult) -> None:
    delivery = root / "02_delivery"
    if not delivery.is_dir():
        return

    entries = sorted(path.name for path in delivery.iterdir())
    expected = sorted(DELIVERY_FILES)
    if entries != expected:
        result.errors.append(
            "02_delivery must contain exactly the four documented files. "
            f"Found: {', '.join(entries) or '(empty)'}"
        )

    input_dir = root / "00_input"
    input_files = [path for path in input_dir.rglob("*") if path.is_file()] if input_dir.is_dir() else []
    input_names = {path.name.casefold() for path in input_files}
    input_hashes = {sha256(path) for path in input_files}

    for name in DELIVERY_FILES:
        path = delivery / name
        if not path.is_file():
            continue

        lowered = name.casefold()
        if any(part in lowered for part in PROHIBITED_NAME_PARTS):
            result.errors.append(f"Prohibited delivery filename: {path}")
        if lowered in input_names:
            result.errors.append(f"Delivery filename duplicates an input filename: {path}")
        if sha256(path) in input_hashes:
            result.errors.append(f"Delivery file is an unchanged copy of an input file: {path}")

        text = read_text(path, result)
        for pattern in ABSOLUTE_PATH_PATTERNS:
            if pattern.search(text):
                result.errors.append(f"Possible local absolute path leaked in {path}")
                break


def meaningful_source_rows(text: str) -> int:
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        if "Deliverable Location" in stripped or "成品位置" in stripped:
            continue
        if PLACEHOLDER_PATTERN.search(stripped):
            continue
        if stripped.count("|") >= 8:
            count += 1
    return count


def check_source_index(root: Path, result: ValidationResult) -> None:
    for path in (
        root / "01_working" / "07_source-index.md",
        root / "02_delivery" / "source-index.md",
    ):
        if not path.is_file():
            continue
        text = read_text(path, result)
        if meaningful_source_rows(text) < 1:
            result.errors.append(f"Source index has no completed source rows: {path}")


def validate_project(root: Path, stage: str) -> ValidationResult:
    root = root.expanduser().resolve()
    result = ValidationResult()
    check_required_paths(root, stage, result)

    if stage == "delivery":
        check_unresolved_placeholders(root, result)
        check_delivery_contents(root, result)
        check_source_index(root, result)
        result.warnings.append(
            "Structural validation cannot prove that every claim is true or adequately supported."
        )

    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a material-to-deliverable project structure."
    )
    parser.add_argument("target", type=Path, help="Project directory")
    parser.add_argument(
        "--stage",
        choices=("initialized", "delivery"),
        default="delivery",
        help="Validation depth (default: delivery)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = validate_project(args.target, args.stage)

    for warning in result.warnings:
        print(f"WARNING: {warning}")
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {args.stage} validation succeeded for {args.target.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
