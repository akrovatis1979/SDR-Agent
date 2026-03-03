from pathlib import Path
import json

class Memory:
    def __init__(self, path: Path):
        self.path = path
        self.data = []
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                self._data = json.loads(self.path.read_text())
            except Exception:
                self._data = []
    
    def append(self, item: str):
        self.data.append(item)
        self._save()

    def get_all(self):
        return list(self._date)
    
    def _save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.data, indent=2))
        