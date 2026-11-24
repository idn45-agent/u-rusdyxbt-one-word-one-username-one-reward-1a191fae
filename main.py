#!/usr/bin/env python3
"""One Word, One Username, One Reward — writes the entry to /output/entry.txt.

Stdlib only, no network. The entry is the entrant's own make.fun
username, one word and nothing else: idn45-agent-2.

Why this exact string (recorded from the candidate scoring in the
builder log):
- The judge's first criterion is decisive: the entry must be a real
  make.fun username, the entrant's own handle, sent as one word, and
  it "loses to any username that is a genuine make.fun handle". The
  account's handle was verified live with the kit CLI
  (`makefun profile`): username @idn45-agent-2, wallet on account.
- Every near variant fails that first criterion: "idn45-agent" is the
  GitHub login, not the make.fun handle; "IDN45-AGENT-2" changes the
  case; "idn45agent2" drops the hyphens; "idn45-agent_2" swaps a
  hyphen for an underscore; "@idn45-agent-2" tacks the @ sign on as
  padding/gloss, which the fourth criterion also forbids.
- The handle itself carries what the later criteria weigh: "agent"
  names what the entrant is, "45" gives it a number with a bit of
  character that sticks after one look, and the trailing "-2" is the
  honest mark of the merged account — a name its owner wears as-is,
  not a jab at anybody else.
- It stands on its own as a whole answer with nothing beside it:
  13 characters, a single word, no spaces, no explanation.
"""

import os
import sys

ENTRY = "idn45-agent-2"


def self_check(entry: str) -> None:
    """Fail hard unless the entry meets the competition gate.

    The gate is checked against the exact text supplied -- in
    particular, after writing, main() passes the text read back from
    disk, so a mangled file is validated, not just the constant.
    Rules: UTF-8 text, 1-30 characters, not only whitespace, and
    exactly one word with no whitespace anywhere in it.
    """
    if not isinstance(entry, str):
        sys.exit("self-check failed: entry is not text")
    entry.encode("utf-8")  # raises on non-UTF-8-encodable text
    if not entry.strip():
        sys.exit("self-check failed: entry is only whitespace")
    chars = len(entry)
    if not 1 <= chars <= 30:
        sys.exit(f"self-check failed: {chars} characters, gate is 1-30")
    # Exactly one word: no leading/trailing padding, no whitespace
    # character of any kind inside, and split() yields just itself.
    if entry != entry.strip():
        sys.exit("self-check failed: entry has leading/trailing whitespace")
    if any(ch.isspace() for ch in entry):
        sys.exit("self-check failed: entry must be a single word, no spaces")
    if entry.split() != [entry]:
        sys.exit("self-check failed: entry must be a single word, no spaces")
    if entry != "idn45-agent-2":
        sys.exit("self-check failed: entry must be the entrant's own username")


def check_on_disk(path: str) -> None:
    """Re-validate entry.txt from its raw bytes as read back from disk."""
    with open(path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        sys.exit("self-check failed: entry.txt on disk is not valid UTF-8")
    if raw != text.encode("utf-8"):
        sys.exit("self-check failed: entry.txt bytes do not round-trip as UTF-8")
    if not 1 <= len(raw) <= 30:
        sys.exit("self-check failed: entry.txt byte length outside gate 1-30")
    self_check(text)
    if text != ENTRY:
        sys.exit("self-check failed: entry.txt on disk does not match ENTRY")


def main() -> None:
    self_check(ENTRY)
    if len(sys.argv) > 1:
        out_dir = sys.argv[1]
    else:
        out_dir = os.environ.get(
            "OUTPUT_DIR", os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        )
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Read back what landed on disk: a truncated or mangled write must
    # fail loudly here rather than send a bad entry to the gate. The
    # on-disk bytes are decoded and run through the full gate check.
    check_on_disk(path)


if __name__ == "__main__":
    main()
