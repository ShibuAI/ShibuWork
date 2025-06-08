from fastapi import FastAPI
from pydantic import BaseModel
import sys
import uvicorn
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from workflows.graph import build_graph


app = FastAPI(title="Gemini Multi-Agent API", version="1.0")

agent_list = [f"agent_{i}" for i in range(1, 11)]
graph = build_graph(agent_list)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = graph.invoke(request.message)
    return {"response": result}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)