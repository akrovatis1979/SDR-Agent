from typing import Optional, Dict, Any
from config import Config
from .tools import Tools
from .memory import Memory

class ResearcherAgent:
    """React-ish agent with Pydantic-validated tool calls + basic decisioning"""
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.tools = Tools(cfg)
        self.memory = Memory(cfg.DATA_DIR / "memory.json")

    def _llm(self, prompt: str) -> str:
        """LLM call placeholder. In production, replace with actual LLM API call."""
        return self._mock_llm(prompt)
    
    def _mock_llm(self, prompt: str) -> str:
        """Simulated LLM that differentiates grounded vs generic prompts for demo clarity"""
        if "Use the following playbook context" in prompt:
            return ("MOCK_LLM_RESPONSE: Grounded output based on playbook context. "
                    "The draft references objection handling and SDR outreach guidance from the"
                    "playbook.")
        return f"MOCK_LLM_RESPONSE: {prompt[:300]} ..."

    def _decide_tool(self, task: str) -> Optional[str]:
        t = task.lower()
        if any(x in t for x in ["calc", "+", "-", "*", "/"]):
            return "calc"
        if "remember" in t:
            return "remember"
        if any(x in t for x in ["playbook", "objection", "qualification", "sales", "cta"]):
            return "rag_retrieve"
        return "search"
    
    def call_tool(self, name: str, args_dict: Dict[str, Any]) -> str:
        if name not in self.tools.registry:
            return f"[tool] unknown tool {name!r}"
        fn, Schema = self.tools.registry[name]
        try:
            args = Schema(**args_dict)
        except Exception as e:
            return f"[tool] {name}] validation error: {e}"
        if name == "remember":
            return fn(args, mem=self.memory)
        return fn(args)
    
    def run(self,
            task: str,
            max_steps: int = 3, 
            tool_name: Optional[str] = None,
            tool_args: Optional[Dict[str, Any]] = None
    ) -> str:
        thoughts = []
        local_args = tool_args
        grounding_chunks: List[Dict[str, Any]] = []

        for i in range(max_steps):
            thoughts.append(f"Step {i+1}: considering -> {task}")
            chosen = tool_name or self._decide_tool(task)

            if not chosen:
                obs = "No tool chosen."
            else:
                if local_args is None:
                    defaults = {
                        "search": {"query": task, "top_k": 3},
                        "calc": {"expression": task.replace("calc", "").strip() or "2+2"},
                        "remember": {"note": task},
                        "rag_retrieve": {"query": task, "k": 3}
                    }
                    local_args = defaults.get(chosen, {})
                obs = self.call_tool(chosen, local_args)

                if chosen == "rag_retrieve":
                    try:
                        grounding_chunks = self.tools.rag.retrieve(task, k=2)
                    except Exception:
                        grounding_chunks = []
                
            thoughts.append(f"Observation: {obs}")
            local_args = None

        context = " ".join(c.get("text", "") for c in grounding_chunks).strip()
        summary_block = "Summarize with citations if present:\n" + "\n".join(thoughts)

        #if context expected here
        return self._llm("Summarize with citations if present:\n" + "\n".join(thoughts))
    
            