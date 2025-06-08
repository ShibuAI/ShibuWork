import streamlit as st 
import os
import sys

# Add parent folder to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from workflows.graph import build_graph

# Initialize the graph
graph = build_graph()

st.set_page_config(layout="wide")
st.title("🧠 Multi-Agent LLM Chat")

# --- Sidebar Agent Selection ---
st.sidebar.header("🔍 Select Agent")
agent_options = ["All Agents", "agent_1", "agent_2", "agent_3", "agent_4", "agent_5"]
selected_agent = st.sidebar.radio("Choose an agent:", agent_options)

# --- Session State Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "graph_state" not in st.session_state:
    st.session_state.graph_state = {
        "message": "",
        "agents_to_call": [],
        "responses": [],
        "current_index": 0,
    }

# --- Display Chat History ---
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# --- User Input ---
prompt = st.chat_input("Ask your multi-agent system...")

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Build agents list based on user selection
    if selected_agent == "All Agents":
        agents_to_call = []  # Let router decide
    else:
        agents_to_call = [selected_agent]

    # Initialize the graph state with new message
    st.session_state.graph_state.update({
        "message": prompt,
        "agents_to_call": agents_to_call,
        "responses": [],
        "current_index": 0,
    })

    try:
        # Invoke graph with current state
        result = graph.invoke(st.session_state.graph_state)
        response = result.get("message", "No response")
        st.session_state.graph_state = result
    except Exception as e:
        response = f"Error invoking graph: {str(e)}"

    st.chat_message("assistant").write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
