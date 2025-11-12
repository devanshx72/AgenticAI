import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph_database_backend import chatbot, retrieve_all_threads
import uuid
import os

os.environ["LANGCHAIN_PROJECT"] = "Streamlit-ChatBot"

# **************************** Utility Functions ****************************

def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    if st.session_state["message_history"] == []:
        return
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    if "messages" in chatbot.get_state(config={"configurable": {"thread_id": thread_id}}).values:
        return chatbot.get_state(config={"configurable": {"thread_id": thread_id}}).values['messages']
    return []


# **************************** Session Setup ****************************
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread(st.session_state["thread_id"])

# **************************** Sidebar UI ****************************

st.sidebar.title("Langgraph ChatBot")
if st.sidebar.button("New Chat"):
    reset_chat()
st.sidebar.header("My Chats")

for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = "user"
            else:
                role = "assistant"
            temp_messages.append({"role": role, "content": msg.content})
        st.session_state["message_history"] = temp_messages

# **************************** Main Chat Interface ****************************

for msg in st.session_state["message_history"]:
    with st.chat_message(msg["role"]):
        st.text(msg["content"])

input = st.chat_input("Enter your message:")

if input:
    st.session_state["message_history"].append({"role": "user", "content": input})
    with st.chat_message("user"):
        st.markdown(f"**You:** {input}")

    # CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {
            "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_turn"
    }

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