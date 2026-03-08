###
import os
from fastapi import FastAPI
from .models import ResearchRequest, EmailRequest, ApprovalRequest
from .rag import RAGTool
from .workflow import Workflow  

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
def approve_workflow(req: ApprovalRequest):
    state = wf.decide(req.work_id, req.decision)
    return state
