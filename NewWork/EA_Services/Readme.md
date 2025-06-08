# 🧠 Multi-Agent LLM Chat with LangGraph + Streamlit

This project is a modular, scalable multi-agent system built using **LangGraph**, **Streamlit**, and **LangChain**, supporting both **OpenAI** and **Google Gemini** LLMs. It dynamically routes user queries to the most appropriate agent based on message content.

---

## 📦 Features

- ✅ Modular Agent Handlers 
- 🔁 Dynamic Agent Routing via LLM
- 🧠 Support for OpenAI and Gemini (switchable)
- 💬 Streamlit Chat Interface
- 🔍 Unit Test Coverage

---

```
multi_agent_project/
├── agents/               # Individual agent logic (e.g. agent_1.py ... agent_10.py)
├── utils/                # LLM switch, router logic
├── workflows/            # LangGraph builder
├── tests/                # Unit tests
├── .env                  # Environment variables
├── app.py                # Streamlit app
├── requirements.txt      # Dependencies
└── README.md
```

### 1. Create Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\activate  # or venv\Scripts\activate on Windows

```

### 2. Set Environment Variables
Create a `.env` file:
```env
LLM_PROVIDER=openai           # or gemini
OPENAI_API_KEY=your-openai-key
GEMINI_API_KEY=your-gemini-key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit App
```bash
streamlit run ui/app.py
```
### 5. Run the Streamlit App
```bash
uvicorn services.api:app --reload
```

LLM_PROVIDER=gemini

# OpenAI config
OPENAI_API_KEY=Your Key
OPENAI_MODEL=gpt-3.5-turbo

# Gemini config
GEMINI_API_KEY=Your Key
GEMINI_MODEL=models/gemini-2.0-flash-thinking-exp