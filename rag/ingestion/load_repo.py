from pathlib import Path
from config import INCLUDE_EXTENSIONS, EXCLUDE_DIRS

def iter_source_files(repo_path: Path):
    """
    Yield source files from a repo path, respecting include/exclude rules.
    Read-only traversal.
    """
    for path in repo_path.rglob("*"):
        # Skip excluded directories anywhere in the path
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue

        # Include only selected extensions
        if path.is_file() and path.suffix in INCLUDE_EXTENSIONS:
            yield path
