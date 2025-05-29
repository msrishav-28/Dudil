import streamlit as st
import os
from datetime import datetime
from utils import (
    load_emotion_model, analyze_emotion, get_emotion_emoji, 
    generate_gemini_response, load_chat_history, save_chat_history, 
    create_new_chat, get_chat_title, setup_gemini_api
)
from sidebar import render_sidebar

st.set_page_config(
    page_title="Dudil",
    page_icon="🤖",
    layout="wide"
)

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = load_chat_history()

    if 'current_chat_id' not in st.session_state:
        st.session_state.current_chat_id = create_new_chat()

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'gemini_model' not in st.session_state:
        st.session_state.gemini_model = None

    if 'api_connected' not in st.session_state:
        st.session_state.api_connected = False

    if 'emotion_data' not in st.session_state:
        with st.spinner("Loading DistilBERT emotion model..."):
            st.session_state.emotion_data = load_emotion_model()
            if st.session_state.emotion_data and st.session_state.emotion_data[0]:
                st.success("Loaded DistilBERT emotion classification model")
            else:
                st.error("Failed to load DistilBERT emotion model")
                st.stop()

def display_chat_messages():
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if not isinstance(message, dict):
                continue
            with st.chat_message(message["role"]):
                st.markdown(message.get("content", ""))
                if message["role"] == "user" and "emotion_analysis" in message:
                    display_emotion_analysis(message["emotion_analysis"])

def display_emotion_analysis(emotion_data):
    emotion = emotion_data.get("emotion", "neutral")
    intensity = emotion_data.get("intensity", emotion_data.get("stars", 3))
    emotion_emoji = get_emotion_emoji(emotion)
    title = f"Emotion Analysis: {emotion.title() if emotion else 'Unknown'} {emotion_emoji}"

    with st.expander(title):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Detected Emotion", emotion.title() if emotion else "Unknown")
        with col2:
            st.metric("Intensity", f"{intensity}/5")
        with col3:
            confidence = emotion_data.get("confidence", 0.0)
            st.metric("Confidence", f"{confidence:.1%}")
        st.caption("Model: DistilBERT Emotion Classification")

def handle_user_input(prompt, api_key):
    if not api_key or not st.session_state.api_connected:
        st.error("Please enter your Gemini API key and connect first.")
        st.stop()

    if not st.session_state.emotion_data or not st.session_state.emotion_data[0]:
        st.error("Emotion model not available")
        st.stop()

    with st.spinner("Analyzing emotion..."):
        emotion_analysis = analyze_emotion(prompt, st.session_state.emotion_data)

    user_message = {
        "role": "user",
        "content": prompt,
        "emotion_analysis": emotion_analysis,
        "timestamp": datetime.now().isoformat()
    }
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(prompt)
        display_emotion_analysis(emotion_analysis)

    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            response = generate_gemini_response(
                prompt, 
                emotion_analysis, 
                st.session_state.messages,
                st.session_state.gemini_model
            )
            st.markdown(response)

    bot_message = {
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().isoformat()
    }
    st.session_state.messages.append(bot_message)

    st.session_state.chat_history[st.session_state.current_chat_id] = {
        'messages': st.session_state.messages,
        'title': get_chat_title(st.session_state.messages),
        'timestamp': datetime.now().isoformat()
    }
    save_chat_history(st.session_state.chat_history)

def setup_api_connection(api_key):
    if api_key and not st.session_state.api_connected:
        with st.spinner("Connecting to Gemini API..."):
            model = setup_gemini_api(api_key)
            if model:
                st.session_state.gemini_model = model
                st.session_state.api_connected = True
                return True
            else:
                st.session_state.api_connected = False
                return False
    return st.session_state.api_connected

def main():
    initialize_session_state()
    api_key = render_sidebar()

    if api_key:
        setup_api_connection(api_key)

    st.title("Please meet Dudil - Your Emotion-Aware Chatbot")

    if st.session_state.messages:
        current_title = get_chat_title(st.session_state.messages)
        st.caption(f"Current chat: {current_title}")

    display_chat_messages()

    model_available = st.session_state.emotion_data and st.session_state.emotion_data[0]
    api_ready = api_key and st.session_state.api_connected

    if prompt := st.chat_input("Type your message here...", disabled=not (api_ready and model_available)):
        handle_user_input(prompt, api_key)

if __name__ == "__main__":
    main()
