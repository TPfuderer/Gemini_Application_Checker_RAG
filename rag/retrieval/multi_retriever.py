from pathlib import Path
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from rag.retrieval.retrieve import Retriever


class MultiProjectRetriever:
    def __init__(self, project_indexes: Dict[str, Path], embedder: SentenceTransformer):
        """
        project_indexes:
            dict: project_name -> index_dir
        """
        self.retrievers = {
            name: Retriever(index_dir=path, embedder=embedder)
            for name, path in project_indexes.items()
        }

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        all_docs = []

        for retriever in self.retrievers.values():
            docs = retriever.retrieve(query, top_k=top_k)
            all_docs.extend(docs)

        # simple relevance trimming
        return all_docs[:top_k]
