from pathlib import Path
from sentence_transformers import SentenceTransformer

from rag.retrieval.retrieve import Retriever
from rag.retrieval.context import build_context
from rag.llm.gemini_client import get_client, generate_answer

QUESTION = "How does this project perform text classification?"

def main():
    project_root = Path(__file__).resolve().parents[1]
    index_dir = project_root / "rag" / "indexes" / "ml_classifier"

    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    retriever = Retriever(index_dir=index_dir, embedder=embedder)

    docs = retriever.retrieve(QUESTION)
    context = build_context(docs)

    client = get_client()
    answer = generate_answer(
        client=client,
        context=context,
        question=QUESTION,
    )

    print("\n--- GROUNDED ANSWER ---\n")
    print(answer)

    print("\n--- CONTEXT USED ---\n")
    print(context)

if __name__ == "__main__":
    main()
