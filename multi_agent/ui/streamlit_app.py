import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agent Chatbot", layout="wide")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

menu = st.sidebar.radio("Navigation", ["Chatbot", "API Responses"])

# Chatbot Page
if menu == "Chatbot":
    st.title("💬 Multi-Agent Chatbot")

    # Chat History Display
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for sender, message in st.session_state.chat_history:
        bubble_class = "user-bubble" if sender == "user" else "bot-bubble"
        align_class = "user" if sender == "user" else "bot"
        icon = "🧑" if sender == "user" else "🤖"
        st.markdown(f"""
            <div class='msg {align_class}'>
                <div class='bubble {bubble_class}'>{icon} {message}</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Input Form for Sending Message
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message:", key="chat_input")
        submitted = st.form_submit_button("Send")

        if submitted and user_input:
            st.session_state.chat_history.append(("user", user_input))
            try:
                
                res = requests.post("http://127.0.0.1:8000/run_agents/", json={"topic": user_input})
                print(f"API Response: {res.status_code} - {res.text}")
                report = res.json().get("report", "🤖 No response generated.")
            except Exception as e:
                report = f"❌ API error: {str(e)}"

            st.session_state.chat_history.append(("bot", report))

elif menu == "API Responses":
    st.title("📊 API Responses Viewer")

    col1, col2, col3 = st.columns(3)
    try:
        with col1:
            st.markdown("### 📞 Call Center")

            with st.form("call_center_form"):
                city = st.text_input("City")
                customer_name = st.text_input("Customer Name")
                customer_id = st.text_input("Customer ID")

                submitted = st.form_submit_button("Fetch Call Center Data")

                if submitted:
                    payload = {}
                    if city:
                        payload["city"] = city
                    if customer_name:
                        payload["customer_name"] = customer_name
                    if customer_id:
                        try:
                            payload["id"] = int(customer_id)
                        except ValueError:
                            st.warning("Customer ID should be an integer.")

                    try:
                        res = requests.post("http://127.0.0.1:8080/call_center", json=payload)
                        res.raise_for_status()
                        call_data = res.json()
                    except Exception as e:
                        call_data = [{"error": str(e)}]

                    st.json(call_data)

        with col2:
            st.markdown("### 📦 Inventory")
            inventory_data = requests.get("http://127.0.0.1:8080/inventory").json()
            st.json(inventory_data)

        with col3:
            st.markdown("### 🖥️ Tech Product")
            tech_data = requests.get("http://127.0.0.1:8080/tech_product").json()
            st.json(tech_data)

    except Exception as e:
        st.error(f"Failed to fetch API response: {e}")
