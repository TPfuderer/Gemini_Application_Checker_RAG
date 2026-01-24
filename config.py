from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PROJECTS = {
    "ML Classifier": {
        "repo_path": BASE_DIR / "projects" / "ml_category_classifier",
        "index_path": BASE_DIR / "rag" / "indexes" / "ml_classifier",
    },
    "OCR Pipeline": {
        "repo_path": BASE_DIR / "projects" / "ocr_pipeline_project",
        "index_path": BASE_DIR / "rag" / "indexes" / "ocr_pipeline",
    },
}


# What to include / exclude during ingestion
INCLUDE_EXTENSIONS = {".py", ".md"}
EXCLUDE_DIRS = {
    ".venv", "__pycache__", "data", "models", "outputs", ".git", ".idea"
}

# RAG parameters
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5
