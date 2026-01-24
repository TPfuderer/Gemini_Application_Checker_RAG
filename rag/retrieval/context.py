from typing import List, Dict

def build_context(docs: List[Dict]) -> str:
    """
    Build a grounded context block for the LLM.

    Each chunk includes:
    - project name
    - source file
    - section title (if available)
    - content text

    This enables explicit citations in answers.
    """
    if not docs:
        return "No relevant project documentation was found."

    blocks = []

    for i, doc in enumerate(docs, start=1):
        header_parts = []

        project = doc.get("project")
        if project:
            header_parts.append(f"Project: {project}")

        source = doc.get("source")
        if source:
            header_parts.append(f"Source: {source}")

        section = doc.get("section_title")
        if section:
            header_parts.append(f"Section: {section}")

        header = " | ".join(header_parts)

        block = f"""
[Context {i}]
{header}
{doc["text"]}
""".strip()

        blocks.append(block)

    return "\n\n".join(blocks)


