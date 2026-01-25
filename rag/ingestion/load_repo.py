from pathlib import Path

def get_readme(repo_path: Path) -> Path | None:
    """
    Return README.md path if it exists, otherwise None.
    """
    readme = repo_path / "README.md"
    return readme if readme.exists() else None

