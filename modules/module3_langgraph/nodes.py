from typing import Dict, List
from modules.module2_rag.retrieval_tool import RAGTool
from modules.module2_rag.actuator import CRMActuator
from config import Config

class LongCRMNode:
    def __init__(self, cfg: Config):
        self.crm = CRMActuator(cfg)

    def run(self, state: Dict) -> Dict:
        self.crm.log_activity({
            "type": "email_draft",
            "prospect": state["prospect"],
            "goal": state["goal"],
            "valid": state.get("valid", False)
        })
        return state