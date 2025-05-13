import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agent Assistant", page_icon="🤖")
st.title("🧠 Multi-Agent Assistant")

topic = st.text_input("Enter a research topic")

if st.button("Run Agents"):
    if not topic.strip():
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Calling multi-agent backend..."):
            try:
                res = requests.post("http://localhost:8000/run_agents/", json={"topic": topic})
                if res.status_code == 200:
                    data = res.json()
                    st.success("Done!")
                    st.subheader("🔍 Summary")
                    st.write(data["summary"])
                    st.subheader("🤔 Critique")
                    st.write(data["critique"])
                    st.subheader("📊 Final Report")
                    st.write(data["report"])
                else:
                    st.error("Failed to get response from API." + str(res.json()))
            except Exception as e:
                st.error(f"Error calling backend: {e}")
