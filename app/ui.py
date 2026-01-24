import streamlit as st
from pathlib import Path
from sentence_transformers import SentenceTransformer

from rag.retrieval.retrieve import Retriever
from rag.retrieval.context import build_context
from rag.llm.gemini_client import get_client, generate_answer

# -------------------------------------------------
# App configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Project Knowledge Assistant",
    layout="wide",
)

st.title("📚 Project Knowledge Assistant")

st.markdown(
    """
This assistant lets you explore how my projects are built.
All answers are **grounded in project documentation and code**
and explicitly reference their source.
"""
)

# -------------------------------------------------
# Resolve project root (path-safe)
# -------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

PROJECTS = {
    "ML Classifier": PROJECT_ROOT / "rag" / "indexes" / "ml_classifier",
    "OCR Pipeline": PROJECT_ROOT / "rag" / "indexes" / "ocr_pipeline",
}

# -------------------------------------------------
# UI controls
# -------------------------------------------------
project_name = st.selectbox(
    "Select project",
    options=list(PROJECTS.keys()),
)

question = st.text_input(
    "Ask a question about this project",
    placeholder="How does this project work?",
)

# -------------------------------------------------
# Core logic
# -------------------------------------------------
if st.button("Ask") and question:
    with st.spinner("Retrieving and reasoning..."):
        embedder = SentenceTransformer("all-MiniLM-L6-v2")

        retriever = Retriever(
            index_dir=PROJECTS[project_name],
            embedder=embedder,
        )

        docs = retriever.retrieve(question, top_k=5)
        context = build_context(docs)

        client = get_client()
        answer = generate_answer(
            client=client,
            context=context,
            question=question,
        )

    st.subheader("Answer")
    st.write(answer)

    with st.expander("Sources used"):
        st.code(context)
