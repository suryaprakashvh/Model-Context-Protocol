from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mcp.registry import TOOLS
import mcp.builtins
from mcp.flow import decide_action
from mcp.llm_handler import ask_llm

app = FastAPI(title="MCP Server with Groq LLM")

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"tools": list(TOOLS.keys())}

@app.post("/query")
def process_query(req: QueryRequest):
    action, params = decide_action(req.query)

    if action == "llm":
        answer = ask_llm(req.query)
        return {"response": answer, "source": "Groq LLM"}

    func = TOOLS.get(action)
    if not func:
        raise HTTPException(status_code=404, detail="Tool not found")

    result = func(**params)
    return {
        "response": format_response(req.query, result),
        "source": "Tool",
        "tool_used": action
    }

def format_response(query: str, result: dict) -> str:
    return f"Query: {query}\nResult: {result}"