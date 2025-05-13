from agents.llm_config import get_llm

def critic_agent(research: str) -> str:
    llm = get_llm()
    return llm.predict(f"Critically evaluate the following research:{research}")