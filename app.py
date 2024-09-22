import streamlit as st
import uuid
from tools import estimate_savings, store_contact_info
from assistant import create_assistant
from graph import build_graph
from utils import print_event


def main():
    st.set_page_config(page_title="Aniket Electronics Ltd. - Smart Thermostat Savings Calculator")
    st.title("Aniket Electronics Ltd. - Smart Thermostat Savings Calculator")

    tools = [estimate_savings, store_contact_info]
    assistant = create_assistant(tools)
    graph = build_graph(assistant, tools)

    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about Smart Thermostat savings"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            config = {
                "configurable": {"thread_id": st.session_state.thread_id},
                "recursion_limit": 50
            }

            events = graph.stream(
                {"messages": ("user", prompt)}, config, stream_mode="values"
            )

            for event in events:
                if 'messages' in event:
                    for message in event['messages']:
                        if hasattr(message, 'content'):
                            full_response += message.content + "\n\n"
                            message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    main()