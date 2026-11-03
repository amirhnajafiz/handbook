"""Validate docs/ against the page template. Exits non-zero on errors.

Checks every docs/<section>[/<subsection>]/NN_name.md for:
  - snake_case, two-digit-prefixed filename
  - exactly one H1
  - the template's H2 sections, in order, with the exact heading text
Warns when the template's dedication placeholder was left in place.
index.md files and sections listed in scripts/.sideignore are skipped.
"""
import os
import re
import sys

DOCS = "docs"
TEMPLATE = "templates/page.md"
NAME_RE = re.compile(r"^\d{2}_[a-z0-9]+(_[a-z0-9]+)*\.md$")
PLACEHOLDER = "Dedication section ..."


def headings(text: str):
    """Yield (level, title) for headings outside fenced code blocks."""
    in_code = False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            in_code = not in_code
        elif not in_code and (m := re.match(r"^(#{1,6})\s+(.*?)\s*$", line)):
            yield len(m.group(1)), m.group(2)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


def ignored_sections() -> set:
    path = "scripts/.sideignore"
    if not os.path.exists(path):
        return set()
    return {l.strip() for l in read(path).splitlines() if l.strip() and not l.startswith("#")}


def main() -> int:
    expected = [t for lvl, t in headings(read(TEMPLATE)) if lvl == 2]
    errors, warnings = [], []
    skip = ignored_sections()

    for root, dirs, files in os.walk(DOCS):
        dirs[:] = sorted(d for d in dirs if d != "images" and not (root == DOCS and d in skip))
        if root == DOCS:
            continue
        if "index.md" not in files:
            errors.append(f"{root}: missing index.md")
        for name in sorted(files):
            if not name.endswith(".md") or name == "index.md":
                continue
            path = os.path.join(root, name)
            if not NAME_RE.match(name):
                errors.append(f"{path}: filename must look like 01_snake_case.md")
            text = read(path)
            hs = list(headings(text))
            if sum(1 for lvl, _ in hs if lvl == 1) != 1:
                errors.append(f"{path}: must have exactly one H1")
            found = [t for lvl, t in hs if lvl == 2]
            if found != expected:
                errors.append(f"{path}: H2 sections must be {expected}, found {found}")
            if PLACEHOLDER in text:
                warnings.append(f"{path}: dedication placeholder still present")

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
