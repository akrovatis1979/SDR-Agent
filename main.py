from config import Config
from modules.module2_rag.data_ingestion import ensure_playbook
from modules.module2_rag.vector_store import TFIDFVectorStore
#from modules.module3_langgraph.graph import SimpleWorkflow

BANNER = """
===========================================================
SDR Agent Automation System (Extended Build)
===========================================================
"""

def main():
    print(BANNER)
    cfg=Config()
    cfg.ensure_dirs()

    print("[Module 2] Ensuring playbook and building RAG Store...")
    ensure_playbook(cfg)
    store = TFIDVectorStore(cfg)
    store.build_or_load()
    print("RAG store ready.")
    print("\n[Module 2] System Initialized Successfully.")

if __name__ == "__main__":
    main()

#Main past version
#from config import Config
#from modules.module2_rag.data_ingestion import ensure_playbook
#from modules.module2_rag.vector_store import TFIDFVectorStore
#from modules.module3_langgraph.graph import SimpleWorkflow
#
#if __name__ == "__main__":
#    from config import Config
#    from modules.module1_react.agent import ResearcherAgent
#
#    print("===========================================================")
#    print("SDR Agent Automation System (Researcher Agent Test)")
#    print("===========================================================")
#
#    cfg = Config()
#    agent = ResearcherAgent(cfg)
#
#    print("[Module 2] Ensuring playbook and building RAG Store...")
#    print("RAG store ready.")
#    print("[Module 3] Building tiny LangGraph workflow...")
#    print("Workflow ready.\n")
#
#    print("System Initialized Successfully")
#
#    # Run one live reasoning task
#    print("Running Researcher Agent...\n")
#    output = agent.run("Find new outreach strategies for SDR teams", max_steps=3)
#    print("\nAgent Output:\n", output)
#
#    print("\n--- Quick Tool Checks ---")
#    print(agent.run("calc 45/5+3", max_steps=1))
#    print(agent.run("remember follow up with Taylor tomorrow", max_steps=1))
#    print(agent.run("playbook objection handling tips", max_steps=2))
