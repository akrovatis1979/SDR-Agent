from typing import List, Dict
from config import Config
from .vector_store import TFIDFVectorStore

class RAGTool:
    def __init__(self, cfg: Config):
        self.store = TFIDFVectorStore(cfg)
        self.store.build_or_load()

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        return [{"text": t, "score": s} for t, s in self.store.query(query, k=k)]

