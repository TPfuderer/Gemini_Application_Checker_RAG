import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH (Streamlit Cloud fix)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


import streamlit as st
from sentence_transformers import SentenceTransformer

from rag.retrieval.retrieve import Retriever
from rag.retrieval.context import build_context
from rag.llm.gemini_client import get_client, generate_answer
from rag.prompts import SYSTEM_PROMPT_ALL, SYSTEM_PROMPT_PROJECT
from config import PROJECTS as PROJECT_CONFIG
from sentence_transformers import util
import config
PROJECT_ROUTING = config.PROJECT_ROUTING



# -------------------------------------------------
# App configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Project Knowledge Assistant",
    layout="wide",
)
st.markdown(
    """
<style>
/* Highlight the question text area */
textarea {
    border: 2px solid #4A90E2 !important;
    border-radius: 6px;
    font-size: 16px;
}

/* Make the Ask button prominent */
div.stButton > button {
    background-color: #4A90E2;
    color: white;
    font-weight: 600;
    padding: 0.6em 1.4em;
    border-radius: 8px;
    border: none;
    font-size: 16px;
}

/* Hover effect for button */
div.stButton > button:hover {
    background-color: #357ABD;
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("📚 Project Knowledge Assistant")


# -------------------------------------------------
# Session state
# -------------------------------------------------
if "query_count" not in st.session_state:
    st.session_state.query_count = 0

MAX_QUERIES_PER_SESSION = 10
MAX_CHUNKS = 10  # keep context small for free-tier stability


# -------------------------------------------------
# Cached resources
# -------------------------------------------------
@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")


# -------------------------------------------------
# Resolve project indexes
# -------------------------------------------------
PROJECTS = {
    name: cfg["index_path"]
    for name, cfg in PROJECT_CONFIG.items()
}

# --- Safety check: routing completeness ---
missing = set(PROJECTS) - set(PROJECT_ROUTING)
if missing:
    st.warning(f"Routing missing for projects: {sorted(missing)}")

PROJECT_OPTIONS = ["All Projects"] + list(PROJECTS.keys())


# -------------------------------------------------
# UI controls
# -------------------------------------------------
project_name = st.selectbox(
    "Select project context",
    options=PROJECT_OPTIONS,
)

if project_name == "All Projects":
    st.info("All Projects mode: evaluates TECHNICAL FIT from project evidence only.")

    st.markdown(
        """
**Limits (Gemini free tier):**
- Limited context per question
- Quality may degrade after several complex queries

**Best usage:**
- Start with 1–2 key technologies or select certain project in the dropdown menu
- Broad multi-skill evaluations may be unreliable
"""
    )

    st.markdown(
        "**Sample questions:**\n"
        "- Does Tristan have experience with [XYZ] technology?\n"
        "- Which projects are relevant for [insert role] ?\n"
        "- Does Tristan fit the following role [role] (based on project evidence only)?"
    )

else:
    st.info(f"Project mode: explains **{project_name}**.")

    st.markdown(
        """
**Scope:**
- Architecture, data flow, tooling, design decisions
- README-based explanations only
"""
    )

    st.markdown(
        "**Sample questions:**\n"
        "- Explain how this project was conducted\n"
        "- What are the main architectural components?\n"
        "- Which engineering decisions stand out?"
    )

question = st.text_area(
    "Ask a question",
    placeholder="e.g. Does Tristan have experience with OCR?",
    height=120,
)

st.caption(
    "Runs on Gemini free tier (limited context). "
    "Paid tier enables larger context and more stable answers."
)


st.caption(
    "ℹ️ Free-tier Gemini usage is rate-limited. "
    "If the model is busy, retry after ~30–60 seconds."
)
st.caption(
    "This demo runs on Gemini's free tier for cost efficiency. "
    "A paid tier would allow larger context windows and more stable responses "
    "across multiple complex queries."
)



# -------------------------------------------------
# Core logic
# -------------------------------------------------
if st.button("Ask question") and question:

    if st.session_state.query_count >= MAX_QUERIES_PER_SESSION:
        st.warning(
            "⚠️ Session limit reached. Please refresh the page to continue."
        )
        st.stop()

    st.session_state.query_count += 1

    with st.spinner("Retrieving and reasoning..."):
        try:
            embedder = load_embedder()
            docs = []

            if project_name == "All Projects":
                # --- Stage 1: project routing ---
                query_emb = embedder.encode(question, convert_to_tensor=True)

                project_scores = []
                for project, desc in PROJECT_ROUTING.items():
                    desc_emb = embedder.encode(desc, convert_to_tensor=True)
                    score = util.cos_sim(query_emb, desc_emb).item()
                    project_scores.append((project, score))

                # Select top 3 most relevant projects
                top_projects = [
                    p for p, _ in sorted(project_scores, key=lambda x: x[1], reverse=True)[:3]
                ]

                # --- Stage 2: retrieve only from selected projects ---
                docs = []
                for project in top_projects:
                    retriever = Retriever(
                        index_dir=PROJECTS[project],
                        embedder=embedder,
                    )
                    project_docs = retriever.retrieve(question, top_k=5)

                    for d in project_docs:
                        d["project"] = project

                    docs.extend(project_docs)

            else:
                retriever = Retriever(
                    index_dir=PROJECTS[project_name],
                    embedder=embedder,
                )
                docs = retriever.retrieve(question, top_k=7)

            # Hard cap context for stability
            docs = docs[:MAX_CHUNKS]

            context = build_context(docs)

            client = get_client()

            system_prompt = (
                SYSTEM_PROMPT_ALL
                if project_name == "All Projects"
                else SYSTEM_PROMPT_PROJECT
            )

            answer = generate_answer(
                client=client,
                context=context,
                question=question,
                system_prompt=system_prompt,
            )

            # Keep compatibility + newline fix
            answer_text = answer[0] if isinstance(answer, tuple) else answer
            st.markdown(answer_text.replace("\\n", "\n"))

            # Model transparency (only if tuple)
            if isinstance(answer, tuple) and len(answer) > 1:
                st.caption(f"🧠 Model used: {answer[1]}")


        except Exception:
            st.error(
                "⚠️ The AI model is temporarily unavailable due to usage limits.\n\n"
                "Please wait ~30–60 seconds and try again."
            )

    with st.expander("Sources used"):
        st.code(context)
