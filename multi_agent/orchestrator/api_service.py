from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agents.multi_agent_graph import build_agent_graph

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
        graph = build_agent_graph()
        result = await graph.ainvoke({"topic": request.topic})
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}

