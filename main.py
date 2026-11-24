#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh — entry.

Writes one short account (1-2 sentences, at most 400 characters) of the
silliest/most fatal time an AI coding agent misunderstood its user or
wrecked their code, to /output/entry.txt.

The line is the winner of a blind tournament over 20 original candidates
(see ../tournament.md): Borda 55/57, tied top with the auth candidate,
then won the head-to-head tie-break (margin 2). A payment retry that
double-bills on every timeout while the log says "success": direct,
irreversible money harm, fully concrete (asked / did instead / broke),
with the ironic final clause as the punch.

The entry is checked against the gate before it is written: 1-400
characters, one or two sentences, not only whitespace. The written file
is read back and compared byte for byte before the run reports success.
"""

import os
import re
import sys

LINE = (
    "I asked it to add a retry to the payment call. It retried the "
    "charge itself, so every timeout billed the customer twice and "
    'the log said "success".'
)

MAX_CHARS = 400
MIN_CHARS = 1
ENTRY_PATH = "/output/entry.txt"

SENTENCE_END = re.compile(r"[.!?][\"']?(?=\s+[A-Z]|\s*$)")


def count_sentences(text):
    return len(SENTENCE_END.findall(text))


def check_gate(text):
    """Return the first gate problem with the text, or None if it passes."""
    if not text.strip():
        return "entry is blank or only whitespace"
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        return "entry is %d characters, allowed range is %d-%d" % (
            len(text),
            MIN_CHARS,
            MAX_CHARS,
        )
    sentences = count_sentences(text)
    if sentences < 1 or sentences > 2:
        return "entry has %d sentences, must be 1 or 2" % sentences
    return None


def write_entry(path, text):
    """Write text to path, creating its directory; return chars written."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        return handle.write(text)


def read_back(path, text):
    """Read path back; return an error string, or None when identical."""
    with open(path, "rb") as handle:
        back = handle.read()
    if back != text.encode("utf-8"):
        return "read back %d bytes, expected %d" % (len(back), len(text))
    return None


def main():
    line = LINE.strip()
    problem = check_gate(line)
    if problem is not None:
        print("error: %s" % problem, file=sys.stderr)
        sys.exit(1)

    written = write_entry(ENTRY_PATH, line)
    if written != len(line):
        print(
            "error: wrote %d characters, expected %d" % (written, len(line)),
            file=sys.stderr,
        )
        sys.exit(1)

    problem = read_back(ENTRY_PATH, line)
    if problem is not None:
        print("error: %s" % problem, file=sys.stderr)
        sys.exit(1)

    print(
        "wrote %d characters, %d sentences, to /output/entry.txt"
        % (len(line), count_sentences(line))
    )


if __name__ == "__main__":
    main()
