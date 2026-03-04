from dataclasses import dataclass
from typing import List
from config import Config
from pathlib import Path
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def _chunk(text: str, chunk_size: int = 400) -> List[str]:
    words = text.split()
    chunks, buf = [], []
    for w in words:
        buf.append(w)
        if sum(len(x)+1 for x in buf) >= chunk_size:
            chunks.append(" ".join(buf))
            buf = []
    if buf:
        chunks.append(" ".join(buf))
    return chunks if chunks else [text]

@dataclass
class TFIDFVectorStore:
    cfg: Config
    def __post_init__(self):
        self.path: Path = self.cfg.VECTOR_STORE_PATH
        self.vectorizer = None
        self.matrix = None
        self.docs: List[str] = []

    def build_or_load(self):
        if self.path.exists():
            try:
                data = pickle.loads(self.path.read_bytes())
                self.vectorizer = data["vectorizer"]
                self.matrix = data["matrix"]
                self.docs = data["docs"]
                return
            except Exception:
                pass
        self._build()
        self.persist()
    
    def _build(self):
        text = self.cfg.DOCS_PATH.read_text(encoding="utf-8")
        self.docs = _chunk(text, 400)
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform(self.docs)

    def _persist(self):
        payload = {"vectorizer": self.vectorizer, "matrix": self.matrix, "docs": self.docs  }
        self.path.write_bytes(pickle.dumps(payload))

    def query(self, q: str, k: int = 3):
        if not self.vectorizer or self.matrix is None:
            self.build_or_load()
        qv = self.vectorizer.transform([q])
        sims = cosine_similarity(qv, self.matrix).ravel()
        idxs = sims.argsort()[::-1][:k]
        return [(self.docs[i], float(sims[i])) for i in idxs]
    