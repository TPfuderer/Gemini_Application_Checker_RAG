from pathlib import Path

# -------------------------------------------------
# Base directory
# -------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent


# -------------------------------------------------
# Canonical project configuration
# Keys = internal project IDs (stable, snake_case)
# display_name = UI-facing label
# -------------------------------------------------
PROJECTS = {
    "ml_category_classifier": {
        "display_name": "ML Classifier",
        "repo_path": Path("projects/ml_category_classifier"),
        "index_path": Path("rag/indexes/ml_classifier"),
    },
    "ocr_pipeline_project": {
        "display_name": "OCR Pipeline",
        "repo_path": Path("projects/ocr_pipeline_project"),
        "index_path": Path("rag/indexes/ocr_pipeline"),
    },
    "active_recall_app": {
        "display_name": "Active Recall App",
        "repo_path": Path("projects/active_recall_app"),
        "index_path": Path("rag/indexes/active_recall_app"),
    },
    "product_show_app": {
        "display_name": "Product Show App",
        "repo_path": Path("projects/product_show_app"),
        "index_path": Path("rag/indexes/product_show_app"),
    },
    "flyer_pipeline_v2": {
        "display_name": "Flyer Pipeline",
        "repo_path": Path("projects/flyer_pipeline_v2"),
        "index_path": Path("rag/indexes/flyer_pipeline"),
    },
    "gemini_application_checker": {
        "display_name": "Gemini Application Checker",
        "repo_path": Path("projects/gemini_application_checker"),
        "index_path": Path("rag/indexes/gemini_application_checker"),
    },
    "candidate_profile": {
        "display_name": "Candidate Profile",
        "repo_path": Path("projects/candidate_profile"),
        "index_path": Path("rag/indexes/candidate_profile"),
    },
}


# -------------------------------------------------
# Semantic routing descriptors (must match PROJECTS keys)
# -------------------------------------------------
PROJECT_ROUTING = {
    "ml_category_classifier": (
        "classical machine learning, TF-IDF, logistic regression, NLP, "
        "text classification, feature engineering, supervised learning, "
        "model training, inference pipelines, reproducibility"
    ),

    "ocr_pipeline_project": (
        "OCR, YOLO, EasyOCR, computer vision, PDF processing, "
        "image pipelines, object detection, text extraction, "
        "document understanding"
    ),

    "gemini_application_checker": (
        "retrieval augmented generation, RAG, vector search, FAISS, "
        "embeddings, semantic search, prompt engineering, "
        "Gemini API, LLM integration, Streamlit deployment"
    ),

    "flyer_pipeline_v2": (
        "end-to-end data pipeline, web scraping, OCR, machine learning, "
        "data ingestion, data cleaning, orchestration, automation, "
        "retail data, ETL pipelines"
    ),

    "product_show_app": (
        "Streamlit app, data visualization, frontend, dashboards, "
        "interactive applications, user interface, "
        "data exploration"
    ),

    "active_recall_app": (
        "database management, spaced repetition, active recall, "
        "learning systems, backend logic, CRUD operations, "
        "application state management"
    ),

    "candidate_profile": (
        "academic background, university coursework, statistics, "
        "data science education, research projects, work experience, "
        "professional profile"
    ),
}


# -------------------------------------------------
# Ingestion controls
# -------------------------------------------------
INCLUDE_EXTENSIONS = {".py", ".md"}

EXCLUDE_DIRS = {
    ".venv",
    "__pycache__",
    "data",
    "models",
    "outputs",
    ".git",
    ".idea",
}


# -------------------------------------------------
# RAG parameters
# -------------------------------------------------
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5


# -------------------------------------------------
# Safety check (fail fast if config is inconsistent)
# -------------------------------------------------
assert set(PROJECTS.keys()) == set(PROJECT_ROUTING.keys()), (
    "PROJECTS and PROJECT_ROUTING keys must match exactly"
)
