from dotenv import load_dotenv
import os

load_dotenv()

def get_llm():
    provider = os.getenv("LLM_PROVIDER", "openai")

    if provider == "openai":
        from langchain.chat_models import ChatOpenAI
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            temperature=0.7,
            max_tokens=1000,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    elif provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash-thinking-exp"),
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.7
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
