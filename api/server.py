from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from modules.module1_react.agent import ResearcherAgent
from modules.module2_rag.retrieval_tool import RAGTool
from modules.module3_langgraph.graph import SimpleWorkflow
from config import Config

app = FastAPI(title="SDR Agent API", version="0.2.0")

cfg = Config()
agent = ResearcherAgent(cfg)
rag = RAGTool(cfg)
wf = SimpleWorkflow(cfg)

class ResearchRequest(BaseModel):
    query: str

class EmailRequest(BaseModel):
    prospect: str
    goal: str

class ApproveRequest(BaseModel):
    work_id: str
    decision: str # "approve" or "reject"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/research")
def research(req: ResearchRequest):
    return {"result": agent.run(req.query, max_steps=3)}

@app.post("/retrieve")
def retrieve(req: ResearchRequest):
    docs = rag.retrieve(req.query, k=3)
    return {"chunks": docs}

@app.post("/generate_email")
def generate_email(req: EmailRequest):
    result = wf.run(prospect=req.prospect, goal=req.goal)
    return result

@app.post("/start_workflow")
def start_workflow(req: EmailRequest):
    state = wf.start(prospect=req.prospect, goal=req.goal)
    return state

@app.post("/approve_workflow")
def approve_workflow(req: ApproveRequest):
    state = wf.decide(req.work_id, req.decision)
    return state
