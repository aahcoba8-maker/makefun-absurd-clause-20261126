#!/usr/bin/env python3
"""The Absurd Clause Contest — one-line entry.

Writes the clause from entry.txt to the output directory the grader
expects (MAKEFUN_OUTPUT_DIR), falling back to /output, then to the
directory next to this script. Verifies the written bytes match the
source before exiting.
"""

import os
import sys

ENTRY_TEXT = (
    "Section 14.2: Any silence lasting longer than four seconds during "
    "a support call shall be construed as acceptance of all future "
    "price increases."
)


def pick_output_dir():
    for candidate in (
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.dirname(os.path.abspath(__file__)),
    ):
        if candidate:
            try:
                os.makedirs(candidate, exist_ok=True)
                probe = os.path.join(candidate, ".write-test")
                with open(probe, "w", encoding="utf-8") as handle:
                    handle.write("ok")
                os.remove(probe)
                return candidate
            except OSError:
                continue
    return os.path.dirname(os.path.abspath(__file__))


def main():
    text = ENTRY_TEXT.strip()
    if not (1 <= len(text) <= 200):
        print(f"entry length {len(text)} outside 1-200", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    out_dir = pick_output_dir()
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(out_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        print("read-back mismatch", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
