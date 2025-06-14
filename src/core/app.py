"""
Dudil Mental Health AI - Main Application
Enhanced mental health support with AI-powered features
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.session_manager import SessionManager
from src.ui.layouts.sidebar_layout import render_sidebar, render_ai_controls
from src.ui.pages import (
    chat_page,
    dashboard_page,
    journal_page,
    exercises_page,
    insights_page,
    crisis_page,
    settings_page
)
from src.utils.helpers import load_custom_css
from config.settings import Settings

# Page configuration must be first Streamlit command
st.set_page_config(
    page_title="Dudil - AI Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://988lifeline.org',
        'Report a bug': 'https://github.com/yourusername/dudil/issues',
        'About': """
        Dudil is an AI-powered mental health companion that provides 
        empathetic support, tracks emotional patterns, and offers 
        personalized wellness recommendations.
        """
    }
)

def initialize_app():
    """Initialize application state and services"""
    # Initialize session manager
    SessionManager.initialize()
    
    # Load custom CSS
    load_custom_css()
    
    # Check for required environment variables
    if not os.getenv("GEMINI_API_KEY") and not st.session_state.get('api_key_provided'):
        st.warning("⚠️ Gemini API key not found in environment. You'll need to provide it in the sidebar.")
    
    # Initialize feature flags
    st.session_state.features = {
        'voice_enabled': Settings.ENABLE_VOICE,
        'ai_therapist': Settings.ENABLE_AI_THERAPIST,
        'mood_prediction': Settings.ENABLE_MOOD_PREDICTION,
        'crisis_detection': Settings.ENABLE_CRISIS_DETECTION
    }

def main():
    """Main application entry point"""
    # Initialize app
    initialize_app()
    
    # Render sidebar and get API key
    api_key = render_sidebar()
    
    # Check if we have API access
    api_connected = st.session_state.get('api_connected', False)
    
    if api_connected:
        # Render AI feature controls in sidebar
        render_ai_controls()
    
    # Get current page from session state
    current_page = st.session_state.get('current_page', 'chat')
    
    # Route to appropriate page
    page_router = {
        'chat': lambda: chat_page.render(api_key),
        'dashboard': lambda: dashboard_page.render(),
        'journal': lambda: journal_page.render(),
        'exercises': lambda: exercises_page.render(),
        'insights': lambda: insights_page.render(),
        'crisis': lambda: crisis_page.render(),
        'settings': lambda: settings_page.render()
    }
    
    # Render the selected page
    if current_page in page_router:
        try:
            page_router[current_page]()
        except Exception as e:
            st.error(f"Error loading page: {str(e)}")
            if Settings.DEBUG:
                st.exception(e)
    else:
        st.error(f"Page '{current_page}' not found")
        
    # Footer
    render_footer()

def render_footer():
    """Render application footer"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        if st.session_state.get('user_id'):
            st.caption(f"Session: {st.session_state.user_id[:8]}...")
    
    with col2:
        st.caption("🧠 Dudil - Your Mental Health AI Companion")
        
    with col3:
        crisis_button = st.button(
            "🆘 Crisis Support",
            key="footer_crisis",
            help="Get immediate crisis support resources"
        )
        if crisis_button:
            st.session_state.current_page = 'crisis'
            st.rerun()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("An unexpected error occurred")
        if Settings.DEBUG:
            st.exception(e)
        else:
            st.error("Please refresh the page or contact support if the problem persists.")