from typing import TypedDict, List
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# Shared state structure
class GraphState(TypedDict):
    message: str
    agents_to_call: List[str]
    responses: List[str]
    current_index: int

# Generic agent handler
def build_agent_handler(agent_name: str):
    def handler(state: GraphState) -> GraphState:
        agent_response = f"{agent_name} processed: {state['message']}"
        new_responses = state.get("responses", []) + [agent_response]
        return {
            "message": state["message"],
            "agents_to_call": state.get("agents_to_call", []),
            "responses": new_responses,
            "current_index": state.get("current_index", 0),
        }
    return handler
