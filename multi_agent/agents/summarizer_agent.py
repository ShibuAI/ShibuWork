from agents.llm_config import get_llm

def summarizer_agent(research: str) -> str:
    llm = get_llm()
    return llm.predict(f"Summarize the following research:{research}")
