import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import chainlit as cl
from agents.multi_agent_graph import build_agent_graph

@cl.on_message
async def main(message: cl.Message):
    topic = message.content.strip()
    await cl.Message(content="🤖 Running agents using LangGraph...").send()
    graph = build_agent_graph()
    result = await graph.ainvoke({"topic": topic})
    await cl.Message(content=f"✅ Final Report:\n\n{result['report']}").send()
