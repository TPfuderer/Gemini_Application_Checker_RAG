"""
Purpose:
Build per-project RAG indexes (FAISS + metadata JSON) from external project repos.

Design:
- Multi-project indexing via config.PROJECTS
- Code chunking: one function = one chunk
- README chunking: one sentence = one chunk
- Embeddings: local sentence-transformers (reproducible, no API cost)
- Vector store: FAISS
- Robust to missing repos: creates an empty index + empty docs JSON

Development approach:
- Core logic and integration are implemented manually.
- AI tools may be used as support for learning and scaffolding, not as an autonomous agent.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

import faiss
from sentence_transformers import SentenceTransformer

from rag.ingestion.parse_readme import parse_markdown_readme
from config import PROJECTS, EMBEDDING_MODEL
from rag.ingestion.load_repo import iter_source_files
from rag.ingestion.parse_code import extract_functions


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _write_docs(docs: List[Dict], out_path: Path) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2, ensure_ascii=False)


def build_index_for_project(
    project_name: str,
    repo_path: Path,
    index_dir: Path,
    embedder: SentenceTransformer,
) -> None:
    _ensure_dir(index_dir)

    docs: List[Dict] = []

    # --- README ingestion (section-level + folder tree) ---
    readme_path = repo_path / "README.md"

    if readme_path.exists():
        readme_chunks = parse_markdown_readme(
            readme_path=readme_path,
            project_name=project_name
        )
        docs.extend(readme_chunks)

    if not repo_path.exists():
        print(f"[WARN] {project_name}: repo_path does not exist: {repo_path}")
    else:
        # Iterate through .py/.md files according to ingestion rules
        for path in iter_source_files(repo_path):
            text = path.read_text(encoding="utf-8", errors="ignore")

            # Python source files -> function chunks
            if path.suffix == ".py":
                lines = text.splitlines()
                for fdef in extract_functions(text):
                    snippet = "\n".join(lines[fdef["start_line"]:fdef["end_line"]]).strip()
                    if not snippet:
                        continue
                    docs.append({
                        "text": snippet,
                        "project": project_name,
                        "source": f"{path.name}::{fdef['name']}",
                        "type": "function",
                        "file": str(path),
                        "symbol": fdef["name"],
                    })


    # Always write docs JSON (even if empty) so downstream never fails
    docs_path = index_dir / "rag_docs.json"
    _write_docs(docs, docs_path)

    # Build FAISS index (even if empty)
    dim = embedder.get_sentence_embedding_dimension()
    index = faiss.IndexFlatL2(dim)

    if len(docs) > 0:
        embeddings = embedder.encode([d["text"] for d in docs])
        index.add(embeddings)
        print(f"[OK] {project_name}: indexed {len(docs)} chunks")
    else:
        print(f"[OK] {project_name}: indexed 0 chunks (empty index created)")

    faiss.write_index(index, str(index_dir / "rag_index.faiss"))


def main():
    embedder = SentenceTransformer(EMBEDDING_MODEL)

    for project_name, cfg in PROJECTS.items():
        repo_path: Path = cfg["repo_path"]
        index_dir: Path = cfg["index_path"]

        build_index_for_project(
            project_name=project_name,
            repo_path=repo_path,
            index_dir=index_dir,
            embedder=embedder,
        )


if __name__ == "__main__":
    main()
