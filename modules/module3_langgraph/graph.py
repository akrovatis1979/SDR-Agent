from typing import Dict
from config import Config
from .nodes import DraftEmailNode, ValidateEmailNode, ReflectNode, ApprovalGateNode, LongCRMNode
from .validation import quality_score
import json, uuid

class SimpleWorkflow:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.draft = DraftEmailNode(cfg)
        self.validate = ValidateEmailNode()
        self.reflect = ReflectNode()
        self.approval = ApprovalGateNode()
        self.logger = LongCRMNode(cfg)
        self.work_dir = self.cfg.DATA_DIR / "work_items"
        self.work_dir.mkdir(parents=True, exist_ok=True)
    
    def run(self, prospect: str, goal: str) -> Dict:
        state = {"prospect": prospect, "goal": goal}
        state = self.draft.run(state)
        state = self.validate.run(state)

        if not state["valid"]:
            state = self.reflect.run(state)
            state = self.validate.run(state) # re-validate after reflection
            if not state["valid"]:
                state["quality"] = quality_score(state.get("draft", ""))
                state["suggestion"] = "Try reducing length and adding a soft CTA."
        state["quality"] = quality_score(state.get("draft", ""))

        state["approval_decision"] = "approve"
        state = self.approval.run(state)
        if state.get("approved"):
            state = self.logger.run(state)
        return state
    
    def start(self, prospect: str, goal: str) -> Dict:
        state = {"prospect": prospect, "goal": goal}
        state = self.draft.run(state)
        state = self.validate.run(state)

        if not state["valid"]:
            state = self. reflect.run(state)
            state = self.validate.run(state) # re-validate after reflection

        state["quality"] = quality_score(state.get("draft", ""))
        state["approval_decision"] = None
        state = self.approval.run(state)

        work_id = str(uuid.uuid4())
        state["work_id"] = work_id
        self.save_state(work_id, state)
        return state
