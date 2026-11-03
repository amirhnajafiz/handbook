import os

def load_sideignore() -> set:
    sideignore_path = os.path.join(".", "scripts/.sideignore")
    if not os.path.exists(sideignore_path):
        print(f"Warning: {sideignore_path} not found.")
        return set()
    
    with open(sideignore_path, 'r', encoding='utf-8') as f:
        return {line.strip() for line in f if line.strip() and not line.startswith('#')}

def list_directories(path: str) -> list:
    ignored = load_sideignore()
    return sorted(
        entry for entry in os.listdir(path)
        if os.path.isdir(os.path.join(path, entry)) and entry not in ignored and entry != "images"
    )

def link_generator(path: str, prefix: str) -> list:
    files = [entry for entry in os.listdir(path) if os.path.isfile(os.path.join(path, entry))]
    
    # only include markdown files (.md) and exclude index.md
    files = [entry for entry in files if entry.endswith('.md') and entry != "index.md"]
    files = [os.path.join(prefix, entry) for entry in files]
    
    return sorted(files)

def get_markdown_title(md_path: str) -> str:
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    return line.lstrip('#').strip()
    except Exception:
        pass
    return os.path.splitext(os.path.basename(md_path))[0]

def section_lines(root: str, directory: str, depth: int) -> list:
    """Sidebar entries for a section: its index, its pages, then its sub-sections."""
    dir_path = os.path.join(root, directory)
    indent = "  " * depth

    # section title comes from its index.md heading
    title = get_markdown_title(os.path.join(dir_path, "index.md"))
    lines = [f"{indent}- [{title}]({directory}/index.md)"]

    for md_file in link_generator(dir_path, directory):
        lines.append(f"{indent}  - [{get_markdown_title(os.path.join(root, md_file))}]({md_file})")

    for sub in list_directories(dir_path):
        for line in section_lines(root, os.path.join(directory, sub), depth + 1):
            lines.append(line)

    return lines

def main():    
    path = "docs"
    output_file = os.path.join(path, "_sidebar.md")

    lines = ["- [Home](home.md)"]
    for directory in list_directories(path):
        lines.extend(section_lines(path, directory, 0))

    # write to sidebar.md
    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

if __name__ == "__main__":
    main()
