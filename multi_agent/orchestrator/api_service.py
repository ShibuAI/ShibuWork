from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agents.build_payload_from_input import build_payload_from_input
from agents.multi_agent_graph import build_agent_graph
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TopicRequest(BaseModel):
    topic: str

@app.post("/run_agents/")
async def run_agents(request: TopicRequest):
    try:
        payload = build_payload_from_input(request.topic)
        print(f"Payload built from input: {payload}")
        graph = build_agent_graph()
        result = await graph.ainvoke({"topic": request.topic})
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

