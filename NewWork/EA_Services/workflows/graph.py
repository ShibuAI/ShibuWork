from typing import TypedDict
from langgraph.graph import StateGraph, END
from utils.common_agent import GraphState
from utils.llm_router import route_to_agent
from agents import agent_1, agent_2, agent_3, agent_4, agent_5

agent_map = {
    "agent_1": agent_1.agent_1_handler,
    "agent_2": agent_2.agent_2_handler,
    "agent_3": agent_3.agent_3_handler,
    "agent_4": agent_4.agent_4_handler,
    "agent_5": agent_5.agent_5_handler,
}

MAX_RECURSION_DEPTH = 20  # set limit less than 25 to avoid recursion error

def router_fn(state: GraphState) -> dict:
    selected_agents = route_to_agent(state["message"], list(agent_map.keys()))
    if not selected_agents:
        selected_agents = list(agent_map.keys())
    print(f"[router_fn] Selected agents: {selected_agents}")
    return {
        "message": state["message"],
        "agents_to_call": selected_agents,
        "responses": [],
        "current_index": 0,
        "recursion_depth": 0,
    }

def agent_chain_fn(state: dict) -> dict:
    idx = state.get("current_index", 0)
    depth = state.get("recursion_depth", 0)
    agents = state.get("agents_to_call", [])
    
    print(f"[agent_chain_fn] idx={idx}, depth={depth}, agents={agents}")
    
    if depth >= MAX_RECURSION_DEPTH:
        print("[agent_chain_fn] Max recursion depth reached, stopping recursion.")
        return state
    
    if idx >= len(agents):
        print("[agent_chain_fn] All agents processed, stopping recursion.")
        return state
    
    agent_name = agents[idx]
    agent_fn = agent_map[agent_name]
    
    # Pass updated recursion depth to agent handler
    updated_state = agent_fn({**state, "recursion_depth": depth + 1})
    
    responses = updated_state.get("responses", [])
    current_message = updated_state.get("message", "")
    
    # Append current agent's response if not empty and not duplicate
    if current_message and (len(responses) == 0 or current_message != responses[-1]):
        responses.append(current_message)
    
    new_state = {
        **updated_state,
        "responses": responses,
        "current_index": idx + 1,  # move to next agent
        "agents_to_call": agents,
        "recursion_depth": depth + 1,
    }
    
    print(f"[agent_chain_fn] New state current_index={new_state['current_index']} recursion_depth={new_state['recursion_depth']}")
    return new_state

def branch_fn(state: dict) -> str:
    idx = state.get("current_index", 0)
    agents = state.get("agents_to_call", [])
    depth = state.get("recursion_depth", 0)
    
    print(f"[branch_fn] idx={idx}, agents_len={len(agents)}, depth={depth}")
    
    if depth >= MAX_RECURSION_DEPTH or idx >= len(agents):
        return "consolidator"
    else:
        return "agent_chain"

def consolidator(state: dict) -> dict:
    combined_message = "\n\n".join(state.get("responses", []))
    print(f"[consolidator] Combined response: {combined_message}")
    return {
        "message": combined_message
    }

def build_graph():
    builder = StateGraph(GraphState)
    builder.add_node("router", router_fn)
    builder.add_node("agent_chain", agent_chain_fn)
    builder.add_node("consolidator", consolidator)

    builder.add_edge("router", "agent_chain")
    builder.add_conditional_edges("agent_chain", branch_fn, {
        "agent_chain": "agent_chain",
        "consolidator": "consolidator"
    })
    builder.add_edge("consolidator", END)

    builder.set_entry_point("router")
    # Uncomment if your langgraph version supports recursion limit config:
    # builder.set_recursion_limit(50)
    return builder.compile()
