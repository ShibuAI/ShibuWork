multi_agent_poc/
│
├── agents/
│   ├── __init__.py
│   ├── research_agent.py
│   ├── summarizer_agent.py
│   ├── critic_agent.py
│   └── presenter_agent.py
│
├── orchestrator/
│   ├── __init__.py
│   ├── chainlit_app.py      # still used for manual Chainlit testing
│   └── api_service.py       # new FastAPI API for agents
│
├── ui/
│   └── streamlit_app.py     # now calls FastAPI backend
│
├── requirements.txt
└── README.md

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

python -m venv venv
.\venv\Scripts\activate

## Setup
1. `pip install -r requirements.txt`
2. Create a `.env` file with OpenAI keys.
3. Run FastAPI backend: `uvicorn orchestrator.api_service:app --reload`
4. Run Streamlit UI: `streamlit run ui/streamlit_app.py`


## Setup
1. Create virtual environment:
   - Windows: `python -m venv venv && .\venv\Scripts\activate`
   - Linux/macOS: `python3 -m venv venv && source venv/bin/activate`

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with OpenAI keys.

4. Run FastAPI backend:
   ```bash
   uvicorn orchestrator.api_service:app --reload
   ```

5. Run Streamlit UI:
   ```bash
   streamlit run ui/streamlit_app.py
   ```
