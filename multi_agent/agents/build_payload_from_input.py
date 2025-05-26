import json
import re
from agents.llm_config import get_llm

def build_payload_from_input(user_input: str) -> dict:
    llm = get_llm()
    prompt = f"""
    Extract a JSON payload for a POST request from the following query:
    "{user_input}"
    
    Only include the keys: City, CustomerName if mentioned.
    Return JSON only.
    """
    response = llm.predict(prompt)
    try:
        print(f"LLM Response: {response}")
        # 🧼 Clean markdown formatting like ```json ... ```
        cleaned = re.sub(r"```(?:json)?|```", "", response).strip()
        payload = json.loads(cleaned)
        print(f"payload: {payload}")
    except Exception as e:
        print(f"Failed to parse payload from LLM: {e}")
        payload = {}

    return payload