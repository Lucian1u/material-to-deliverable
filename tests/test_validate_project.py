from __future__ import annotations

import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from init_project import WORKING_FILES, initialize_project  # noqa: E402
from validate_project import DELIVERY_FILES, validate_project  # noqa: E402


PLACEHOLDER_PATTERN = re.compile(r"\{\{[^{}]+\}\}")


def fill_template(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = PLACEHOLDER_PATTERN.sub("filled", text)
    path.write_text(text, encoding="utf-8")


def complete_project(project: Path) -> None:
    initialize_project(project)
    input_file = project / "00_input" / "source.md"
    input_file.write_text("source material", encoding="utf-8")

    for name in WORKING_FILES:
        fill_template(project / "01_working" / name)

    mapping = {
        "main-deliverable.md": "05_main-deliverable.md",
        "one-page-summary.md": "06_one-page-summary.md",
        "source-index.md": "07_source-index.md",
    }
    for destination, source in mapping.items():
        shutil.copyfile(
            project / "01_working" / source,
            project / "02_delivery" / destination,
        )
    (project / "02_delivery" / "readme.md").write_text(
        "# Delivery\n\nStatus: ready\n",
        encoding="utf-8",
    )


class ValidateProjectTests(unittest.TestCase):
    def test_skill_frontmatter_matches_directory(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        frontmatter = text.split("---", 2)[1]
        fields = {}
        for line in frontmatter.splitlines():
            if ":" not in line or line.startswith(" "):
                continue
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')

        self.assertEqual(fields.get("name"), ROOT.name)
        self.assertTrue(fields.get("description"))
        self.assertEqual(fields.get("license"), "MIT")

    def test_initialized_stage_passes_with_templates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            initialize_project(project)
            result = validate_project(project, "initialized")
            self.assertTrue(result.ok, result.errors)

    def test_completed_delivery_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            complete_project(project)
            result = validate_project(project, "delivery")
            self.assertTrue(result.ok, result.errors)
            self.assertTrue(result.warnings)

    def test_unresolved_placeholder_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            complete_project(project)
            path = project / "02_delivery" / "readme.md"
            path.write_text("{{UNRESOLVED}}", encoding="utf-8")

            result = validate_project(project, "delivery")
            self.assertFalse(result.ok)
            self.assertTrue(any("Unresolved placeholders" in error for error in result.errors))

    def test_extra_delivery_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            complete_project(project)
            (project / "02_delivery" / "chat-log.md").write_text("internal", encoding="utf-8")

            result = validate_project(project, "delivery")
            self.assertFalse(result.ok)
            self.assertTrue(any("exactly the four" in error for error in result.errors))

    def test_absolute_path_leak_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            complete_project(project)
            path = project / "02_delivery" / "readme.md"
            path.write_text("See /Users/private-name/project/source.md", encoding="utf-8")

            result = validate_project(project, "delivery")
            self.assertFalse(result.ok)
            self.assertTrue(any("absolute path" in error for error in result.errors))

    def test_unchanged_input_copy_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            complete_project(project)
            source = project / "00_input" / "source.md"
            shutil.copyfile(source, project / "02_delivery" / "readme.md")

            result = validate_project(project, "delivery")
            self.assertFalse(result.ok)
            self.assertTrue(any("unchanged copy" in error for error in result.errors))

    def test_all_behavioral_fixtures_exist(self) -> None:
        for name in ("normal", "sparse", "conflicting", "sensitive"):
            fixture = ROOT / "tests" / "fixtures" / name / "00_input"
            self.assertTrue(fixture.is_dir())
            self.assertTrue(any(path.is_file() for path in fixture.iterdir()))

        sensitive = (
            ROOT / "tests" / "fixtures" / "sensitive" / "00_input" / "customer-record.md"
        ).read_text(encoding="utf-8")
        self.assertIn("privacy-test@example.com", sensitive)


if __name__ == "__main__":
    unittest.main()
