from utils.common import get_llm
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

template = """You are a router. Based on the user's message, choose the best agent.

Available agents:
{agent_list}

Message: {message}
Agent name (exact):"""

prompt = PromptTemplate.from_template(template)
llm = get_llm()
router_chain = LLMChain(llm=llm, prompt=prompt)

# def route_to_agent(message: str, agent_list: list) -> str:
#     agent_str = "\n".join(agent_list)
#     result = router_chain.run(message=message, agent_list=agent_str)
#     return result.strip()

def route_to_agent(message: str, agents: list[str]) -> list[str]:
    # Simple example logic returning multiple agents based on keywords
    message_lower = message.lower()
    selected = []
    if "billing" in message_lower:
        selected.extend(["agent_1", "agent_3"])
    if "support" in message_lower:
        selected.append("agent_2")
    if "sales" in message_lower:
        selected.append("agent_4")
    if "technical" in message_lower:
        selected.append(["agent_3", "agent_5"])
    # If none matched, call all agents by default
    if not selected:
        return agents
    return selected