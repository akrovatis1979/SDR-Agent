from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    """Input model for the new search tool."""
    query: str = Field(..., description="Search query string")
    top_k: int = Field(3, ge=1, le=10, description="How many results to summarize")
    
class CalcInput(BaseModel):
    """Input model for the calculator tool."""
    expression: str = Field(..., description="Arithmetic expression like '5*7+3'")

def MemoryInput(BaseModel):
    """Input model for writing to agent memory."""
    note: str = Field(..., description="Short memory note to store")

def RAGInput(BaseModel):
    """Input model for retrieving information via RAG"""
    query: str = field(..., description="RAG retrieval query")
    k: int = Field(3, ge=1, le=10, description="How many chunks to return")