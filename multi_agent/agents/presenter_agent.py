from agents.llm_config import get_llm

def presenter_agent(summary: str, critique: str) -> str:
    llm = get_llm()
    return llm.predict(f"Combine this summary and critique into a report:Summary: {summary} Critique: {critique}")