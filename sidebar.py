import streamlit as st
import os
from datetime import datetime
from utils import setup_gemini_api, create_new_chat, get_chat_title, save_chat_history

def render_sidebar():
    """Render the complete sidebar with API configuration and chat management"""
    with st.sidebar:
        st.title("🤖 Dudil Emotion-Aware Chat")

        api_key = os.getenv("GEMINI_API_KEY")
        handle_api_connection(api_key)

        st.divider()
        handle_new_chat()

        st.divider()
        render_chat_history()

    return api_key

def handle_api_connection(api_key):
    """Handle API connection logic"""
    if api_key and not st.session_state.api_connected:
        model = setup_gemini_api(api_key)
        if model:
            st.session_state.gemini_model = model
            st.session_state.api_connected = True
        else:
            st.session_state.gemini_model = None
            st.session_state.api_connected = False

    if api_key and not st.session_state.api_connected:
        st.error("❌ Failed to connect to Gemini API")
        if st.button("🔄 Retry Connection"):
            st.session_state.api_connected = False
            st.session_state.gemini_model = None
            st.rerun()

def handle_new_chat():
    """Handle new chat creation"""
    if st.button("➕ New Chat", use_container_width=True):
        if st.session_state.messages:
            st.session_state.chat_history[st.session_state.current_chat_id] = {
                'messages': st.session_state.messages,
                'title': get_chat_title(st.session_state.messages),
                'timestamp': datetime.now().isoformat()
            }
            save_chat_history(st.session_state.chat_history)

        st.session_state.current_chat_id = create_new_chat()
        st.session_state.messages = []
        st.rerun()

def render_chat_history():
    """Render chat history section"""
    st.subheader("📚 Chat History")

    if st.session_state.chat_history:
        if st.button("🗑️ Clear All History", use_container_width=True):
            if st.button("⚠️ Confirm Clear All", use_container_width=True, key="confirm_clear"):
                st.session_state.chat_history = {}
                save_chat_history(st.session_state.chat_history)
                st.success("All chat history cleared!")
                st.rerun()

        st.divider()

        recent_chats = list(st.session_state.chat_history.items())[-10:]
        for chat_id, chat_data in reversed(recent_chats):
            if not isinstance(chat_data, dict):
                continue
            render_chat_item(chat_id, chat_data)
    else:
        st.info("No chat history yet. Start chatting to create history!")

def render_chat_item(chat_id, chat_data):
    col1, col2 = st.columns([3, 1])

    with col1:
        chat_title = chat_data.get('title', 'Untitled Chat')
        timestamp = chat_data.get('timestamp', 'Unknown')[:16]

        if st.button(
            f"💬 {chat_title}",
            key=f"load_{chat_id}",
            use_container_width=True,
            help=f"Created: {timestamp}"
        ):
            if st.session_state.messages:
                st.session_state.chat_history[st.session_state.current_chat_id] = {
                    'messages': st.session_state.messages,
                    'title': get_chat_title(st.session_state.messages),
                    'timestamp': datetime.now().isoformat()
                }

            st.session_state.current_chat_id = chat_id
            st.session_state.messages = chat_data.get('messages', [])
            save_chat_history(st.session_state.chat_history)
            st.rerun()

    with col2:
        if st.button("🗑️", key=f"delete_{chat_id}", help="Delete this chat"):
            if chat_id == st.session_state.current_chat_id:
                st.session_state.current_chat_id = create_new_chat()
                st.session_state.messages = []

            del st.session_state.chat_history[chat_id]
            save_chat_history(st.session_state.chat_history)
            st.success("Chat deleted!")
            st.rerun()
