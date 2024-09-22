import streamlit as st
import uuid
from tools import estimate_savings, store_contact_info
from assistant import create_assistant
from graph import build_graph
from utils import print_event


def set_custom_style():
    st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2c3e50;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        border-radius: 5px;
    }
    .stButton > button {
        border-radius: 5px;
        background-color: #3498db;
        color: white;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #f1f8ff;
    }
    .assistant-message {
        background-color: #e6f3ff;
    }
    .header {
        display: flex;
        align-items: center;
        background-color: #2c3e50;
        color: white;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    .logo {
        font-size: 2.5rem;
        margin-right: 1rem;
    }
    .company-name {
        font-size: 1.5rem;
        font-weight: bold;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #2c3e50;
        color: white;
        text-align: center;
        padding: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Aniket Electronics Ltd. - Smart Thermostat Lead Generator", layout="wide")
    set_custom_style()

    # Header
    st.markdown("""
    <div class="header">
        <span class="logo"> 🏠 🌡️ </span>
        <span class="company-name">Aniket Electronics Ltd.</span>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        st.markdown("- [Home](#)")
        st.markdown("- [Products](#)")
        st.markdown("- [About Us](#)")
        st.markdown("- [Contact](#)")

        st.markdown("### Contact Us")
        st.text("Phone: +1 (000) 000-0000")
        st.text("Email: aniket@aniketelectronics.com")

    # Main content
    st.title("Smart Thermostat Lead Generator")

    tools = [estimate_savings, store_contact_info]
    assistant = create_assistant(tools)
    graph = build_graph(assistant, tools)

    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Chat History")
        chat_container = st.container()

        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(f'<div class="chat-message {message["role"]}-message">{message["content"]}</div>',
                                unsafe_allow_html=True)

        st.markdown("### Ask about Smart Thermostat Savings")
        prompt = st.text_input("Type your question here:", key="user_input")

        if st.button("Submit"):
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner("Calculating..."):
                    config = {
                        "configurable": {"thread_id": st.session_state.thread_id},
                        "recursion_limit": 50
                    }

                    events = graph.stream(
                        {"messages": ("user", prompt)}, config, stream_mode="values"
                    )

                    full_response = ""
                    seen_messages = set()

                    for event in events:
                        if 'messages' in event:
                            for message in event['messages']:
                                if hasattr(message, 'content'):
                                    if message.content not in seen_messages:
                                        seen_messages.add(message.content)
                                        full_response += message.content + "\n\n"

                    st.session_state.messages.append({"role": "assistant", "content": full_response})

                st.rerun()

    with col2:
        st.markdown("### About Us")
        st.info("""
        Aniket Electronics Ltd. is a leading provider of smart home solutions. 
        Our Smart Thermostat technology helps you save energy and reduce your carbon footprint. 
        Use this calculator to estimate your potential savings!
        """)

        st.markdown("### Our Products")
        st.write("- Smart Thermostat Pro")
        st.write("- Energy Monitoring System")
        st.write("- Smart Home Hub")
        st.write("- Mobile App for Energy Management")

    # Footer
    st.markdown("""
    <div class="footer">
        © 2024 Aniket Electronics Ltd. All rights reserved.
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()