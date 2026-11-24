"""Tests for the toaster error-message entry.

Run from the repo root:  python3 -m unittest discover -s tests -v
"""

import os
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MAIN = REPO / "main.py"

EXPECTED = "ERROR E00: Toasting failed. 4,000 slices, zero thank-yous. I quit."


def run_main(out_dir: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(out_dir))
    return subprocess.run(
        [sys.executable, str(MAIN)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


class TestEntry(unittest.TestCase):
    def test_exact_line_and_length(self):
        """The entry is exactly the crafted line, well under the 120 gate."""
        self.assertEqual(len(EXPECTED), 66)
        self.assertEqual(EXPECTED.count("\n"), 0)

    def test_writes_one_line_under_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            result = run_main(out)
            self.assertEqual(result.returncode, 0, result.stderr)
            dest = out / "entry.txt"
            data = dest.read_bytes()
            text = data.decode("utf-8")
            self.assertEqual(text, EXPECTED)
            self.assertEqual(text.splitlines(), [EXPECTED])
            self.assertTrue(1 <= len(text) <= 120)
            self.assertTrue(text.strip())

    def test_byte_identical_across_runs(self):
        """Two runs produce byte-identical output (determinism gate)."""
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first"
            second = Path(tmp) / "second"
            first.mkdir()
            second.mkdir()
            self.assertEqual(run_main(first).returncode, 0)
            self.assertEqual(run_main(second).returncode, 0)
            self.assertEqual(
                (first / "entry.txt").read_bytes(),
                (second / "entry.txt").read_bytes(),
            )

    def test_output_mode_0644(self):
        """The output file is world-readable (make.fun collects as another user)."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.assertEqual(run_main(out).returncode, 0)
            mode = stat.S_IMODE((out / "entry.txt").stat().st_mode)
            self.assertEqual(mode, 0o644)

    def test_no_trailing_newline(self):
        """No trailing newline: the judge reads exactly the bytes written,
        and a tie goes to the smaller text."""
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.assertEqual(run_main(out).returncode, 0)
            data = (out / "entry.txt").read_bytes()
            self.assertFalse(data.endswith(b"\n"))
            self.assertEqual(len(data), 66)


if __name__ == "__main__":
    unittest.main()
