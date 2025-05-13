from agents.llm_config import get_llm

def research_agent(topic: str) -> str:
    llm = get_llm()
    return llm.predict(f"Research the following topic in detail: {topic}")