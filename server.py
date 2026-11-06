from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn
import os
import sys

# Add the project root to sys.path to allow imports from api.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from api import OmniControlAPI

app = FastAPI(title="OmniControl Brain-Link Server")
control_api = OmniControlAPI()

class ToolCall(BaseModel):
    tool: str
    args: Optional[Dict[str, Any]] = {}

@app.get("/")
async def root():
    return {"status": "online", "message": "OmniControl Brain-Link is active."}

@app.get("/tools")
async def list_tools():
    """Returns the list of tools available for the AI to use."""
    return {"tools": control_api.get_tool_definitions()}

@app.post("/execute")
async def execute_tool(call: ToolCall):
    """
    Executes a tool call from the AI.
    Example: {"tool": "click", "args": {"x": 500, "y": 200}}
    """
    # Convert Pydantic model to dictionary for the engine
    tool_payload = {
        "tool": call.tool,
        "args": call.args if call.args else {}
    }

    result = control_api.execute(tool_payload)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result

if __name__ == "__main__":
    # Run server on localhost:8000
    # To make it "Live" (externally accessible), change "127.0.0.1" to "0.0.0.0"
    # and use a tool like ngrok or a VPN to expose the port.
    uvicorn.run(app, host="127.0.0.1", port=8000)
