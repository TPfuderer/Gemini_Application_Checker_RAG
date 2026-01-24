from pathlib import Path
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, index_dir: Path, embedder: SentenceTransformer):
        self.index_dir = index_dir
        self.embedder = embedder

        self.index = faiss.read_index(str(index_dir / "rag_index.faiss"))
        with open(index_dir / "rag_docs.json", "r", encoding="utf-8") as f:
            self.docs = json.load(f)

    def retrieve(self, query: str, top_k: int = 5):
        query_vec = self.embedder.encode([query])
        distances, indices = self.index.search(query_vec, top_k * 2)

        candidates = []
        for idx in indices[0]:
            if idx == -1:
                continue
            doc = self.docs[idx]

            priority = 0
            if doc.get("source") == "folder_tree":
                priority = 3
            elif doc.get("source") == "README.md":
                priority = 2
            elif doc.get("type") == "function":
                priority = 1

            candidates.append((priority, doc))

        candidates.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in candidates[:top_k]]

