from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.runnables import RunnableLambda
from agents.research_agent import research_agent
from agents.summarizer_agent import summarizer_agent
from agents.critic_agent import critic_agent
from agents.presenter_agent import presenter_agent

class AgentState(dict):
    topic: str = ""
    research: str = ""
    summary: str = ""
    critique: str = ""
    report: str = ""

def build_agent_graph():
    graph = StateGraph(AgentState)

    graph.add_node("research_node", RunnableLambda(lambda state: {"research": research_agent(state["topic"])}))
    graph.add_node("summarize_node", RunnableLambda(lambda state: {"summary": summarizer_agent(state["research"])}))
    graph.add_node("critique_node", RunnableLambda(lambda state: {"critique": critic_agent(state["research"])}))
    graph.add_node("present_node", RunnableLambda(lambda state: {"report": presenter_agent(state["summary"], state["critique"])}))

    graph.set_entry_point("research_node")
    graph.add_edge("research_node", "summarize_node")
    graph.add_edge("research_node", "critique_node")
    graph.add_edge("summarize_node", "present_node")
    graph.add_edge("critique_node", "present_node")
    graph.add_edge("present_node", END)
        


    return graph.compile()
