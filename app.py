import streamlit as st
from graph import app
from langchain_core.messages import HumanMessage

st.set_page_config(page_title="Retail AI Assistant", layout="wide")

st.title("🛍️ Retail AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask about products or returns...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            state = {
                "messages": [HumanMessage(content=user_input)]
            }

            result = app.invoke(state)
            response = result["messages"][-1].content

            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})