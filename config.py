from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

PROJECTS = {
    "ML Classifier": {
        "repo_path": Path("projects/ml_category_classifier"),
        "index_path": Path("rag/indexes/ml_classifier"),
    },
    "OCR Pipeline": {
        "repo_path": Path("projects/ocr_pipeline_project"),
        "index_path": Path("rag/indexes/ocr_pipeline"),
    },
    "Active Recall App": {
        "repo_path": Path("projects/active_recall_app"),
        "index_path": Path("rag/indexes/active_recall_app"),
    },
    "Product Show App": {
        "repo_path": Path("projects/product_show_app"),
        "index_path": Path("rag/indexes/product_show_app"),
    },
    "Flyer Pipeline": {
        "repo_path": Path("projects/flyer_pipeline_v2"),
        "index_path": Path("rag/indexes/flyer_pipeline"),
    },
    "Gemini Application Checker": {
        "repo_path": Path("projects/gemini_application_checker"),
        "index_path": Path("rag/indexes/gemini_application_checker"),
    },
    "Candidate Profile": {
        "repo_path": Path("projects/candidate_profile"),
        "index_path": Path("rag/indexes/candidate_profile"),
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
