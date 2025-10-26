import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

st.title("ChatBot with LangGraph")
CONFIG = {"configurable": {"thread_id": "chatbot_thread"}}

# Initialize session state for message history
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

for msg in st.session_state["message_history"]:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])

input = st.chat_input("Enter your message:")

if input:
    st.session_state["message_history"].append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.markdown(f"**You:** {input}")

    human_message = {"messages": [HumanMessage(content=input)]}
    response = chatbot.invoke(human_message, config=CONFIG)
    response_message = response["messages"][-1].content
    st.session_state["message_history"].append({"role": "assistant", "content": response_message})
    with st.chat_message("assistant"):
        st.markdown(response_message)


