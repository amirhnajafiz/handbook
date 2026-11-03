"""Create a new page from templates/page.md and regenerate the sidebar.

Usage: python3 scripts/new_page.py <section> "<Title>"

<section> is a directory under docs/, optionally nested like storage_systems/ceph
(missing directories are created, each with an index.md).
The page is numbered after the last page in the section: docs/<section>/NN_<slug>.md.
"""
import os
import re
import subprocess
import sys

TEMPLATE = "templates/page.md"
DOCS = "docs"


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def next_number(section_dir: str) -> int:
    nums = [
        int(m.group(1))
        for f in os.listdir(section_dir)
        if (m := re.match(r"^(\d+)_.*\.md$", f))
    ]
    return max(nums, default=0) + 1


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)

    parts = [slugify(p) for p in sys.argv[1].split("/")]
    title = sys.argv[2].strip()
    if not all(parts) or not slugify(title):
        sys.exit("error: section and title must contain letters or digits")

    section_dir = DOCS
    for part in parts:
        section_dir = os.path.join(section_dir, part)
        if not os.path.isdir(section_dir):
            os.makedirs(section_dir)
            with open(os.path.join(section_dir, "index.md"), "w", encoding="utf-8") as f:
                f.write(f"# {part.replace('_', ' ').title()}\n")
            print(f"created section {section_dir}/index.md")

    with open(TEMPLATE, encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r"^# Title$", lambda _: f"# {title}", content, count=1, flags=re.M)

    path = os.path.join(section_dir, f"{next_number(section_dir):02d}_{slugify(title)}.md")
    if os.path.exists(path):
        sys.exit(f"error: {path} already exists")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"created {path}")

    subprocess.run([sys.executable, "scripts/side_generator.py"], check=True)
    print("sidebar regenerated")


if __name__ == "__main__":
    main()
