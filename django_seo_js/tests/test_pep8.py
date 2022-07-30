import unittest
import os
import pep8


class TestCodeFormat(unittest.TestCase):

    def test_pep8_conformance(self):
        """Test that we conform to PEP8."""
        ALL_FILES = []
        IGNORED_CODES = ["E501", "E226", "E302", "E41", "E128", "E127", ]

        project_root = os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..",
            "..",
        ))
        ignored_folders = [
            ".git",
            "venv",
            ".tox",
        ]

        pep8style = pep8.StyleGuide(
            # quiet=True,
            report=pep8.StandardReport,
            show_source=True,
            max_line_length=120,
        )
        for code in IGNORED_CODES:
            pep8style.ignore_code(code)

        for root, dirnames, filenames in os.walk(project_root):
            if all(folder not in root for folder in ignored_folders):
                ALL_FILES.extend(
                    os.path.join(root, filename)
                    for filename in filenames
                    if filename[-3:] == ".py"
                )

        result = pep8style.check_files(ALL_FILES)

        self.assertEqual(
            result.total_errors,
            0,
            f"Found {result.total_errors} code style errors (and warnings).",
        )
