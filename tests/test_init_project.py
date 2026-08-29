from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from init_project import InitError, WORKING_FILES, initialize_project  # noqa: E402


class InitProjectTests(unittest.TestCase):
    def test_initializes_expected_structure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            created = initialize_project(project)

            self.assertTrue((project / "00_input").is_dir())
            self.assertTrue((project / "01_working").is_dir())
            self.assertTrue((project / "02_delivery").is_dir())
            for name in WORKING_FILES:
                self.assertTrue((project / "01_working" / name).is_file())
            self.assertEqual(len(created), 3 + len(WORKING_FILES))

    def test_preserves_existing_input_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            input_dir = project / "00_input"
            input_dir.mkdir(parents=True)
            source = input_dir / "source.md"
            source.write_text("real input", encoding="utf-8")

            initialize_project(project)

            self.assertEqual(source.read_text(encoding="utf-8"), "real input")

    def test_refuses_to_overwrite_working_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            initialize_project(project)
            task_brief = project / "01_working" / "01_task-brief.md"
            task_brief.write_text("user work", encoding="utf-8")

            with self.assertRaises(InitError):
                initialize_project(project)

            self.assertEqual(task_brief.read_text(encoding="utf-8"), "user work")

    def test_refuses_nonempty_delivery_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "project"
            delivery = project / "02_delivery"
            delivery.mkdir(parents=True)
            existing = delivery / "existing.md"
            existing.write_text("keep", encoding="utf-8")

            with self.assertRaises(InitError):
                initialize_project(project)

            self.assertEqual(existing.read_text(encoding="utf-8"), "keep")


if __name__ == "__main__":
    unittest.main()
