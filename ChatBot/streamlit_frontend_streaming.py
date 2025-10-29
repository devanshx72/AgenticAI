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

    # st.session_state["message_history"].append({"role": "assistant", "content": response_message})
    with st.chat_message("assistant"):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {"messages": HumanMessage(content=input)},
                config=CONFIG,
                stream_mode="messages"
            )
        )

        st.session_state["message_history"].append({"role": "assistant", "content": ai_message})