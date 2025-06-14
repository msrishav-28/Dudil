"""
Session state management for Dudil Mental Health AI
Handles user sessions, state persistence, and initialization
"""

import streamlit as st
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json
import os
from pathlib import Path

class SessionManager:
    """Centralized session state management"""
    
    # Default session values
    DEFAULTS = {
        'user_id': None,
        'session_id': None,
        'current_page': 'chat',
        'messages': [],
        'chat_history': {},
        'current_chat_id': None,
        'api_connected': False,
        'gemini_model': None,
        'emotion_data': None,
        'mental_health_analyzer': None,
        'voice_analyzer': None,
        'ai_features_enabled': False,
        'user_preferences': {
            'theme': 'dark',
            'notifications': True,
            'anonymous_mode': False,
            'voice_enabled': True
        },
        'temp_data': {},
        'last_activity': None
    }
    
    @classmethod
    def initialize(cls):
        """Initialize session state with defaults"""
        # Set defaults for any missing keys
        for key, default_value in cls.DEFAULTS.items():
            if key not in st.session_state:
                if key == 'user_id':
                    st.session_state[key] = cls._generate_user_id()
                elif key == 'session_id':
                    st.session_state[key] = cls._generate_session_id()
                elif key == 'last_activity':
                    st.session_state[key] = datetime.now()
                else:
                    st.session_state[key] = default_value
        
        # Initialize components that need special handling
        cls._initialize_components()
        
        # Check session timeout
        cls._check_session_timeout()
        
        # Load persisted data if available
        cls._load_persisted_data()
    
    @classmethod
    def _generate_user_id(cls) -> str:
        """Generate a unique user ID"""
        # Check if we have a stored user ID (for returning users)
        stored_id = cls._get_stored_user_id()
        if stored_id:
            return stored_id
        
        # Generate new ID
        new_id = f"user_{uuid.uuid4().hex[:16]}"
        cls._store_user_id(new_id)
        return new_id
    
    @classmethod
    def _generate_session_id(cls) -> str:
        """Generate a unique session ID"""
        return f"session_{uuid.uuid4().hex[:16]}"
    
    @classmethod
    def _initialize_components(cls):
        """Initialize special components"""
        # Only initialize if not already present
        if 'component_init' not in st.session_state:
            st.session_state.component_init = {
                'emotion_model': False,
                'mental_health': False,
                'voice': False,
                'ai_features': False
            }
    
    @classmethod
    def _check_session_timeout(cls):
        """Check if session has timed out"""
        if st.session_state.last_activity:
            timeout_minutes = 60  # 1 hour default
            time_since_activity = datetime.now() - st.session_state.last_activity
            
            if time_since_activity > timedelta(minutes=timeout_minutes):
                # Session timeout - clear sensitive data
                cls.clear_session()
                st.warning("Your session has timed out for security. Please reconnect.")
    
    @classmethod
    def _load_persisted_data(cls):
        """Load persisted user data if available"""
        try:
            # Load chat history
            chat_history_path = Path("data/chat_history.json")
            if chat_history_path.exists():
                with open(chat_history_path, 'r') as f:
                    data = json.load(f)
                    if st.session_state.user_id in data:
                        st.session_state.chat_history = data[st.session_state.user_id]
            
            # Load user preferences
            preferences_path = Path(f"data/users/{st.session_state.user_id}/preferences.json")
            if preferences_path.exists():
                with open(preferences_path, 'r') as f:
                    st.session_state.user_preferences = json.load(f)
                    
        except Exception as e:
            # Silently fail - not critical
            pass
    
    @classmethod
    def update_activity(cls):
        """Update last activity timestamp"""
        st.session_state.last_activity = datetime.now()
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """Get value from session state"""
        cls.update_activity()
        return st.session_state.get(key, default)
    
    @classmethod
    def set(cls, key: str, value: Any):
        """Set value in session state"""
        cls.update_activity()
        st.session_state[key] = value
    
    @classmethod
    def update(cls, updates: Dict[str, Any]):
        """Update multiple values in session state"""
        cls.update_activity()
        for key, value in updates.items():
            st.session_state[key] = value
    
    @classmethod
    def clear_session(cls):
        """Clear session data (logout)"""
        # Preserve user_id for returning users
        user_id = st.session_state.get('user_id')
        
        # Clear everything
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        # Reinitialize with preserved user_id
        st.session_state.user_id = user_id
        cls.initialize()
    
    @classmethod
    def save_chat_history(cls):
        """Save chat history to persistent storage"""
        try:
            chat_history_path = Path("data/chat_history.json")
            chat_history_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Load existing data
            existing_data = {}
            if chat_history_path.exists():
                with open(chat_history_path, 'r') as f:
                    existing_data = json.load(f)
            
            # Update with current user's data
            existing_data[st.session_state.user_id] = st.session_state.chat_history
            
            # Save back
            with open(chat_history_path, 'w') as f:
                json.dump(existing_data, f, indent=2, default=str)
                
        except Exception as e:
            # Log error but don't crash
            st.warning("Could not save chat history")
    
    @classmethod
    def save_preferences(cls):
        """Save user preferences"""
        try:
            user_dir = Path(f"data/users/{st.session_state.user_id}")
            user_dir.mkdir(parents=True, exist_ok=True)
            
            preferences_path = user_dir / "preferences.json"
            with open(preferences_path, 'w') as f:
                json.dump(st.session_state.user_preferences, f, indent=2)
                
        except Exception:
            pass
    
    @classmethod
    def create_new_chat(cls) -> str:
        """Create a new chat session"""
        chat_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
        st.session_state.current_chat_id = chat_id
        st.session_state.messages = []
        return chat_id
    
    @classmethod
    def switch_chat(cls, chat_id: str):
        """Switch to a different chat"""
        if chat_id in st.session_state.chat_history:
            st.session_state.current_chat_id = chat_id
            st.session_state.messages = st.session_state.chat_history[chat_id].get('messages', [])
        else:
            st.warning("Chat not found")
    
    @classmethod
    def delete_chat(cls, chat_id: str):
        """Delete a chat from history"""
        if chat_id in st.session_state.chat_history:
            del st.session_state.chat_history[chat_id]
            
            # If deleting current chat, create new one
            if chat_id == st.session_state.current_chat_id:
                cls.create_new_chat()
            
            # Save updated history
            cls.save_chat_history()
    
    @classmethod
    def _get_stored_user_id(cls) -> Optional[str]:
        """Get stored user ID from local storage"""
        try:
            user_id_path = Path("data/.user_id")
            if user_id_path.exists():
                with open(user_id_path, 'r') as f:
                    return f.read().strip()
        except:
            pass
        return None
    
    @classmethod
    def _store_user_id(cls, user_id: str):
        """Store user ID for returning users"""
        try:
            user_id_path = Path("data/.user_id")
            user_id_path.parent.mkdir(parents=True, exist_ok=True)
            with open(user_id_path, 'w') as f:
                f.write(user_id)
        except:
            pass
    
    @classmethod
    def export_user_data(cls) -> Dict[str, Any]:
        """Export all user data for download"""
        return {
            'user_id': st.session_state.user_id,
            'export_date': datetime.now().isoformat(),
            'chat_history': st.session_state.chat_history,
            'preferences': st.session_state.user_preferences,
            'sessions': {
                'total': len(st.session_state.chat_history),
                'current': st.session_state.current_chat_id
            }
        }
    
    @classmethod
    def import_user_data(cls, data: Dict[str, Any]):
        """Import user data from backup"""
        try:
            if 'chat_history' in data:
                st.session_state.chat_history = data['chat_history']
            
            if 'preferences' in data:
                st.session_state.user_preferences = data['preferences']
            
            # Save imported data
            cls.save_chat_history()
            cls.save_preferences()
            
            return True
        except Exception as e:
            st.error(f"Failed to import data: {str(e)}")
            return False