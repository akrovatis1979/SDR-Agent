from typing import Dict, List
from modules.module2_rag.retrieval_tool import RAGTool
from modules.module2_rag.actuator import CRMActuator
from config import Config

class DraftEmailNode:
    def __init__(self, cfg: Config):
        self.rag = RAGTool(cfg)

    def run(self, state: Dict) -> Dict:
        prospect = state["prospect"]
        goal = state["goal"]

        # Retrieve supporting playbook chunks
        support = self.rag.retrieve(f"{prospect} outreach best practices {goal}", k=2)

        # Build short, explicit citations from the playbook chunks
        citation_lines: List[str] = []
        for idx, c in enumerate(support, start=1):
            snippet = c["text"].replace("\n", " ").strip()[:120]
            citation_lines.append(f"[Playbook {idx}] {snippet}")

        citations_text = "\n".join(citation_lines) if citation_lines else "[No playbook references found]"

        draft = (
            f"Hi {prospect},\n\n"
            f"I'm reaching out to share a quick idea to help you with {goal}.\n\n"
            f"According to our sales playbook:\n{citations_text}\n\n"
            f"If you're open to it, happy to send a 2-minute summary.\n"
            f"- SDR Team"
        )

        state["draft"] = draft
        state["citations"] = citation_lines # keep raw list too (useful for UI/tests)
        return state
    
class ValidateEmailNode:
    def run(self, state: Dict) -> Dict:
        draft = state.get("draft", "")
        ok_length = len(draft) <= 800
        has_cta = "happy to send" in draft.lower() or "interested" in draft.lower()
        state["valid"] = ok_length and has_cta
        state["issues"] = []
        if not ok_length:
            state["issues"].append("Email too long.")
        if not has_cta:
            state["issues"].append("Missing soft CTA.")
        return state
    
class ReflectNode:
    def run(self, state: Dict) -> Dict:
        draft = state.get("draft", "")

        # Enforce a soft CTA if missing
        if "happy to send" not in draft.lower():
            draft += "\n\nIf helpful, I'm happy to send a 2-minute summary."

        # Shorten if needed
        if len(draft) > 800:
            draft = draft[:780] + "..."

        state["draft"] = draft
        state["reflected"] = True
        return state
    
class ApprovalGateNode:
    def run(self, state: Dict) -> Dict:
        decision = state.get("approval_decision") # "approve" | "reject" | None
        if decision in ("approve", "reject"):
            state["awaiting_approval"] = False
            state["approved"] = (decision == "approve")
            return state
        # pause for human approval
        state["awaiting_approval"] = True
        state["approved"] = False
        return state

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