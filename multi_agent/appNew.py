import streamlit as st
import os
import sys

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from workflows.graph import build_graph

# Set Streamlit layout
st.set_page_config(page_title="🧠 Multi-Agent LLM Chat", layout="wide")
st.title("💬 Conversational Multi-Agent Chat")

# --- Sidebar ---
st.sidebar.header("🧠 Choose Agent")
agent_options = [
    "All Agents", "Architect Assist", "Automated Mappings", 
    "Enterprise Architecture Common Agents", "Investment Planning",
    "Strategic Partnership", "Technology Convergence", "Vendor Product Mgmt"
]
selected_agent = st.sidebar.radio("Select Target Agent", agent_options)

# --- Init Graph & State ---
if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

st.session_state.setdefault("messages", [])
st.session_state.setdefault("graph_state", {
    "message": "",
    "agents_to_call": [],
    "responses": [],
    "current_index": 0
})

# --- Chat Bubble Styling ---
st.markdown("""
    <style>
        .chat-bubble { max-width: 80%; padding: 10px 15px; border-radius: 20px; margin-bottom: 10px; display: inline-block; }
        .user { background-color: #dcf8c6; margin-left: auto; }
        .bot { background-color: #f1f0f0; margin-right: auto; }
        .default-question {
            background-color: #e6f2ff;
            padding: 8px 12px;
            border-radius: 15px;
            cursor: pointer;
            display: inline-block;
            margin: 5px 10px 5px 0;
        }
        .default-question:hover {
            background-color: #cce6ff;
        }
    </style>
""", unsafe_allow_html=True)

# --- Show Chat History ---
st.markdown("### 💬 Conversation")
for msg in st.session_state.messages:
    style = "user" if msg["role"] == "user" else "bot"
    emoji = "🧑" if msg["role"] == "user" else "🤖"
    st.markdown(f"<div class='chat-bubble {style}'><b>{emoji}:</b> {msg['content']}</div>", unsafe_allow_html=True)

# --- Default Suggestions if Empty ---
if not st.session_state.messages:
    st.markdown("#### 🧠 Try asking:")
    default_qs = [
        "What is the current investment plan status?",
        "Show me vendor product spend insights",
        "Help me with enterprise architecture issues",
        "Explain technology convergence plan"
    ]
    cols = st.columns(len(default_qs))
    for i, q in enumerate(default_qs):
        if cols[i].button(q):
            st.session_state["chat_input"] = q  # Pre-fill input box
            st.experimental_rerun()

# --- User Input Form ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Ask your question:", key="chat_input")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Save user prompt
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare agents
    agents_to_call = [] if selected_agent == "All Agents" else [selected_agent]
    st.session_state.graph_state.update({
        "message": user_input,
        "agents_to_call": agents_to_call,
        "responses": [],
        "current_index": 0
    })

    # Try invoking graph
    try:
        result = st.session_state.graph.invoke(st.session_state.graph_state)
        response = result.get("message") or result.get("report") or "🤖 No response."
        st.session_state.graph_state = result
    except Exception as e:
        response = "🤖 Sorry, I couldn't process that. Could you rephrase?"

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.experimental_rerun()
