import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

def get_llm(model: str = None, temperature: float = 0.0):
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set.")
        return ChatOpenAI(model_name=model or "gpt-4", temperature=temperature, api_key=api_key)

    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set.")
        return ChatGoogleGenerativeAI(model=model or "gemini-pro", temperature=temperature, google_api_key=api_key)

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")