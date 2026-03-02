from typing import Dict, Tuple
from .schemas import SearchInput, CalcInput, MemoryInput, RAGInput
from modules.module2_rag.retrieve_tool import RAGTool
from config import Config

class Tools:
    """Central registry for all validated tools used by the SDR Agent.
    
    Each tool method performs a small, well-defined task such as searching,
    calulating, writing to memory, or retrieving data via RAG. Tools are
    registered with their corresponding Pydantic input schemas.
    """

    def __init__(self, cfg: Config):
        """Innitialize the tools registry and supporting modules."""
        self.cfg = cfg
        self.rag_tool = RAGTool(cfg)
        self.registry: Dict[str, Tuple] = {
            "search": (self._search, SearchInput),
            "calc": (self._calc, CalcInput),
            "remember": (self._memory_write, MemoryInput),
            "rag_retrieve": (self._rag_retrieve, RAGInput),
        }

    def _search(self, args: SearchInput) -> str:
        """Simulate a web search.
        
        Args:
            args: A SearchInput object with:
                - query (str): search query text
                - top_k (int): number of results to summarize
                
        Returns:
            A short string describing what woulb be search and summarized.
        """
        return f"[search] Would look up: {args.query!r} and summarize top {args.top_k} results."

    def _calc(self, args: CalcInput) -> str:
        """Evaluate a simple arithmetic expression safely.
        
        Only digits, spaces, and + - * / ( ) are allowed.
        
        Args:
            args: A CalcInput object with:
                - expression (str): e.g., "15*3+2"
                
        Returns:
            The computed result as a string, or an error message prefixed with 'calc_error:'.
        """
        try:
            allowed = set("0123456789+-*/(). ")
            if not set(args.expression) <= allowed:
                return "calc_error: disallowed characters"
            return str(eval(args.expression, {"__builtins__": {}}, {}))
        except Exception as e:
            return f"calc_error: {str(e)}"
        
    def _memory_write(self, args: MemoryInput) -> str:
        """Append a note to short-term memory.
        
        Args:
            args: A MemoryInput object with:
                - note (str): the note to store
            mem: A list-like memory store provided by the agent.
        
        Returns:
            'memory: noted' on success, or an error if memory was not provided.
        """
        if mem is None:
            return "memory error: no memory provided"
        mem.append(args.note)
        return "memory: noted"
    
    def _rag_retrieve(self, args: RAGInput) -> str:
        """Retrieve relevant playbook chunks from the RAG store.
        
        Args:
            args: A RAGInput object with:
                - query (str): retrieval query
                - top_k (int): number of chunks to return
                
        Returns:
            A compact string of scored snippets like "[0.534] snippet... | [0.412] snippet
        """
        chunks = self.rag.retrieve(args.query, k=args.k)
        return " | ".join(f"[{round(c['score'], 3)}] {c['text'][:200]}..." for c in chunks)
    