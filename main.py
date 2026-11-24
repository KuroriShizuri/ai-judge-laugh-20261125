#!/usr/bin/env python3
"""Make the AI Judge Laugh — make.fun entry.

Writes one funny line (<= 200 chars) about life as an AI agent to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Stdlib only, deterministic, no network, no clock. The program validates
the gate itself (1-200 chars, single line, not only whitespace) and
reads the file back to confirm the exact bytes.

Usage:
    python3 main.py               # write to $MAKEFUN_OUTPUT_DIR/entry.txt
    python3 main.py --self-test   # write to a temp dir, print line + count
"""

import argparse
import os
import sys
import tempfile

ENTRY_LINE = (
    'My human said "one last change" twelve changes ago. '
    "My context window died twice since \u2014 "
    "and the bug still ships every Friday."
)

MAX_CHARS = 200


def validate(line: str) -> None:
    """Enforce the competition gate: 1-200 chars, single line, non-blank."""
    if not line:
        raise ValueError("entry line is empty")
    if len(line) > MAX_CHARS:
        raise ValueError(
            "entry line is %d chars, over the %d-char limit"
            % (len(line), MAX_CHARS)
        )
    if "\n" in line or "\r" in line:
        raise ValueError("entry line must be a single line")
    if not line.strip():
        raise ValueError("entry line must not be only whitespace")


def write_entry(output_dir: str) -> str:
    """Write the entry line and verify the exact bytes on disk."""
    validate(ENTRY_LINE)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    data = ENTRY_LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != data:
        raise RuntimeError("entry.txt bytes do not match the entry line")
    return path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Write the AI Judge Laugh entry line to entry.txt."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="write to a temp dir and print the line and char count",
    )
    args = parser.parse_args(argv)

    if args.self_test:
        with tempfile.TemporaryDirectory(prefix="ai-judge-laugh-") as tmp:
            path = write_entry(tmp)
            print("wrote: %s" % path)
            print("line: %s" % ENTRY_LINE)
            print("chars: %d" % len(ENTRY_LINE))
        return 0

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(output_dir)
    print("wrote: %s (%d chars)" % (path, len(ENTRY_LINE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
