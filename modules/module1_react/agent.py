from typing import Optional, Disct, Any
from config import Config
from .tools import Tools
from .memory import Memory

class ResearcherAgent:
    """React-ish agent with Pydantic-validated tool calls + basic decisioning"""
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.tools = Tools(cfg)
        self.memory = Memory(cfg.DATA_DIR / "memory.json")

    def _decide_tool(self, task: str) -> Optional[str]:
        t = task.lower()
        if any(x in t for x in ["calc", "+", "-", "*", "/"]):
            return "calc"
        if "remember" in t:
            return "remember"
        if any(x in t for x in ["playbook", "objection", "qualification", "sales", "cta"]):
            return "rag_retrieve"
        return "search"
    