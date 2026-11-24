#!/usr/bin/env python3
"""The Funniest Toaster Error Message entry.

Writes one fixed error line to /output/entry.txt: the toaster's own
complaint, in the shape of a real appliance error (code + failure +
status). Python 3.13, standard library only. Deterministic: the output
bytes are exactly the LINE string below, on every run. No network,
no randomness, no trailing newline (the judge reads exactly the bytes
written, and a tie goes to the smaller text).
"""

import os
from pathlib import Path

LINE = "ERROR E00: Toasting failed. 4,000 slices, zero thank-yous. I quit."


def main() -> None:
    # Guardrail: the gate takes UTF-8 text of 1-120 characters, not only
    # whitespace. Fail loudly here instead of writing an invalid entry.
    if not 1 <= len(LINE) <= 120:
        raise SystemExit(f"line is {len(LINE)} characters, outside the 1-120 gate")
    if not LINE.strip():
        raise SystemExit("line is only whitespace")
    if "\n" in LINE or "\r" in LINE:
        raise SystemExit("line must be exactly one line")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # The grader runs this as a different user against a root-owned
    # output dir: chmod on the directory raises PermissionError there,
    # so tolerate it — the file chmod below is what the collector needs.
    try:
        os.chmod(out_dir, 0o755)
    except OSError:
        pass
    dest = out_dir / "entry.txt"
    dest.write_text(LINE, encoding="utf-8")
    # make.fun collects outputs as another user: the file must be readable
    # by everyone, so force 0644 regardless of umask.
    os.chmod(dest, 0o644)
    # Read back and verify the exact bytes the judge will see.
    if dest.read_bytes() != LINE.encode("utf-8"):
        raise SystemExit(f"verify failed: {dest} does not match the line bytes")
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
