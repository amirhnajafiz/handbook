"""Normalize page filenames in docs/: snake_case, fixed typos, sequential NN_ prefixes.

Usage: python3 scripts/normalize_names.py [--apply]
Without --apply it only prints the planned renames.
"""
import os
import re
import subprocess
import sys

DOCS = "docs"
TYPOS = {"upd": "udp", "consistancy": "consistency", "sateful": "stateful"}


def clean(stem: str) -> str:
    stem = re.sub(r"^\d+_", "", stem).lower().replace("-", "_")
    return "_".join(TYPOS.get(w, w) for w in stem.split("_"))


def plan() -> list:
    moves = []
    for d in sorted(os.listdir(DOCS)):
        dp = os.path.join(DOCS, d)
        if not os.path.isdir(dp):
            continue
        pages = sorted(f for f in os.listdir(dp) if f.endswith(".md") and f != "index.md")
        for i, f in enumerate(pages, 1):
            new = f"{i:02d}_{clean(os.path.splitext(f)[0])}.md"
            if new != f:
                moves.append((os.path.join(dp, f), os.path.join(dp, new)))
    return moves


def main():
    moves = plan()
    for a, b in moves:
        print(f"{a} -> {b}")
    if "--apply" not in sys.argv:
        return
    # two-phase to avoid collisions when shifting numbers
    for i, (a, _) in enumerate(moves):
        subprocess.run(["git", "mv", a, f"{a}.tmp{i}"], check=True)
    for i, (a, b) in enumerate(moves):
        subprocess.run(["git", "mv", f"{a}.tmp{i}", b], check=True)


if __name__ == "__main__":
    main()
