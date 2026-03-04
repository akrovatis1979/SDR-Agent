from config import Config
from modules.module2_rag.data_ingestion import ensure_playbook
from modules.module2_rag.vector_store import TFIDFVectorStore
from modules.module3_langgraph.graph import SimpleWorkflow

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
