from config import Config
from modules.module2_rag.data_ingestion import ensure_playbook
from modules.module2_rag.vector_store import TFIDFVectorStore
from modules.module3_langgraph.graph import SimpleWorkflow

if __name__ == "__main__":
    from config import Config
    from modules.mopdule1_react.agent import ResearcherAgent

    print("=============================================================================" \
    print("SDR Agent Automation System (Researcher Agent Test)")
    print("=============================================================================\n")

    cfg = Config()
    agent = ResearcherAgent(cfg)

    print("[Module 2] Ensuring playbook and building RAG store...")
    print("RAG store ready.")
    print("[Module 3] Building tiny LangGraph workflow...")
    print("Workflow ready.\n")

    print("System Initialized Successfully!\n")

    # Run one live reasoning task
    print("Running Researcher Agent...\n")
    output = agent.run("Find new outreach strategies for SDR teams", max_steps=3)
    print("\nAgent Output:\n", output)

    print("\n--- Quick Tool Checks ---")
    print(agent.run("calc 45/5+3", max_steps=1))
    print(agent.run("remember follow up with Taylor tomorrow", max_steps=1))
    print(agent.run("playbook objection handling tips", max_steps=2))

