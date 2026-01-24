import re
from pathlib import Path

def parse_markdown_readme(readme_path: Path, project_name: str):
    """
    Parse a Markdown README into section-level chunks.

    Returns a list of dicts with:
    - text
    - project
    - section_title
    - source
    """

    text = readme_path.read_text(encoding="utf-8")

    # Split on markdown headers (# or ##)
    sections = re.split(r"\n(?=##?\s)", text)

    chunks = []

    for section in sections:
        lines = section.strip().splitlines()
        if not lines:
            continue

        header_line = lines[0]

        if header_line.startswith("#"):
            section_title = header_line.lstrip("#").strip()
            body = "\n".join(lines[1:]).strip()
        else:
            section_title = "Introduction"
            body = section.strip()

        if not body:
            continue

        chunks.append({
            "text": body,
            "project": project_name,
            "section_title": section_title,
            "source": "README.md"
        })

    return chunks

def build_folder_tree(root_path, max_depth=4):
    """
    Build a readable folder tree as text.
    """

    lines = []

    def walk(path, prefix="", depth=0):
        if depth > max_depth:
            return

        entries = sorted(
            [p for p in path.iterdir() if p.name != "__pycache__"],
            key=lambda x: (x.is_file(), x.name.lower())
        )

        for i, entry in enumerate(entries):
            connector = "└── " if i == len(entries) - 1 else "├── "
            lines.append(prefix + connector + entry.name)

            if entry.is_dir():
                extension = "    " if i == len(entries) - 1 else "│   "
                walk(entry, prefix + extension, depth + 1)

    lines.append(root_path.name)
    walk(root_path)

    return "\n".join(lines)

