#!/usr/bin/env python3
"""Entry for make.fun bounty "One Star, Five Stars for the Food".

An alien tourist hands planet Earth a one-star review and still
admits the food was excellent. This program writes exactly that
one sentence, 1 to 200 characters, as UTF-8 text to entry.txt in
the output directory, with no trailing newline. The judge then
compares it pairwise against the other entries, weighing the
complaint, the food compliment, and how convincingly alien the
voice sounds.

The program holds the sentence as a constant, checks it against
the gate before writing anything, and writes it byte-for-byte. If
it ever drifted outside the gate, it fails loudly instead of
producing an invalid entry. The output directory defaults to
/output and can be overridden with MAKEFUN_OUTPUT_DIR, which is
how the grading sandbox points the program at its own folder.
"""

import os
import sys
from pathlib import Path

ENTRY = 'One star: the locals scream about lizard people and stare at the sky, but the tacos? We abducted the recipe, the cook, and the truck.'

MAX_CHARS = 200


def validate(text: str) -> None:
    """Enforce the gate: 1-200 characters, one line, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")


def write_entry(text: str, out_dir: Path) -> None:
    """Write the validated line to entry.txt, with no trailing newline."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # write_text writes exactly these bytes: no trailing newline added.
    (out_dir / "entry.txt").write_text(text, encoding="utf-8")


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    text = ENTRY.strip()
    try:
        validate(text)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    write_entry(text, out_dir)
    print(text)
    print(f"wrote entry.txt ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
