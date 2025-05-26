# agents/context_agent.py
from agents.llm_config import get_llm
from agents.data_fetch_agent import (
    fetch_call_center_data,
    fetch_inventory_data,
    fetch_tech_product_data,
)

def contextual_response(topic: str) -> str:
    llm = get_llm()
    print(f"Fetching data for topic: {topic}")
    if "call center" in topic.lower():
        data = fetch_call_center_data()
    elif "inventory" in topic.lower():
        data = fetch_inventory_data()
    elif "tech" in topic.lower():
        data = fetch_tech_product_data()
    else:
        data = []

    prompt = f"Topic: {topic}\nRelevant Data: {data[:5]}\n\nRespond to user:"
    return llm.predict(prompt)
