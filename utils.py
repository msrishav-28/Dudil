import json
import os
from datetime import datetime
import google.generativeai as genai
from transformers import pipeline
import streamlit as st
from dotenv import load_dotenv



load_dotenv()

CHAT_HISTORY_FILE = "chat_history.json"

@st.cache_resource
def load_emotion_model():
    try:
        model_name = os.getenv("DISTILBERT_MODEL")
        emotion_pipeline = pipeline(
            "text-classification",
            model=model_name,
            return_all_scores=True
        )
        return emotion_pipeline, "distilbert-emotion"
    except Exception as e:
        st.error(f"Failed to load DistilBERT emotion model: {e}")
        return None, None

def setup_gemini_api():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found in environment variables")
        return None
    
    try:
        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL")
        model = genai.GenerativeModel(model_name)
        return model
    except Exception as e:
        st.error(f"Failed to setup Gemini API: {e}")
        return None

def analyze_emotion(text, emotion_model_data):
    if emotion_model_data is None or emotion_model_data[0] is None:
        st.error("DistilBERT emotion model not available")
        return {"emotion": "neutral", "confidence": 0.0, "intensity": 3, "model_type": "none"}
    
    emotion_pipeline, model_type = emotion_model_data
    
    try:
        if not text or not text.strip():
            return {"emotion": "neutral", "confidence": 0.5, "intensity": 3, "model_type": model_type}
            
        results = emotion_pipeline(text[:512])
        
        if isinstance(results, list) and len(results) > 0:
            if isinstance(results[0], list):
                results = results[0]
        
        best_result = max(results, key=lambda x: x['score'])
        emotion = best_result['label'].lower()
        confidence = best_result['score']
        
        emotion_to_intensity = {
            'joy': 5,
            'love': 5, 
            'surprise': 4,
            'anger': 2,
            'fear': 2,
            'sadness': 1
        }
        
        intensity = emotion_to_intensity.get(emotion, 3)
            
        return {
            "emotion": emotion,
            "confidence": confidence,
            "intensity": intensity,
            "raw_results": results,
            "model_type": model_type
        }
    except Exception as e:
        st.error(f"Emotion analysis error: {e}")
        return {"emotion": "neutral", "confidence": 0.0, "intensity": 3, "model_type": model_type}

def get_emotion_emoji(emotion):
    emotion_emoji_map = {
        'joy': "😊",
        'love': "😍", 
        'surprise': "😮",
        'anger': "😠",
        'fear': "😨",
        'sadness': "😢",
        'neutral': "😐"
    }
    return emotion_emoji_map.get(emotion.lower(), "😐")

def generate_gemini_response(user_message, emotion_analysis, conversation_history, gemini_model):
    if gemini_model is None:
        return "I'm sorry, I couldn't connect to the AI service. Please check your API key."
    
    try:
        emotion = emotion_analysis.get("emotion", "neutral")
        intensity = emotion_analysis.get("intensity", 3)
        confidence = emotion_analysis.get("confidence", 0.0)
        
        emotion_context = f"""You are a helpful and empathetic AI assistant. The user's message has been analyzed for emotions:
                            - Detected emotion: {emotion}
                            - Intensity: {intensity}/5
                            - Confidence: {confidence:.1%}

                            Respond appropriately based on their emotional state:
                            - Joy: Be enthusiastic and share their positive feelings
                            - Love: Be warm and supportive of their affection
                            - Sadness: Be empathetic, comforting, and supportive  
                            - Anger: Be calm, understanding, and help them process feelings
                            - Fear: Be reassuring and help alleviate concerns
                            - Surprise: Be engaging and explore their reaction""".strip()
        
        history_context = ""
        if len(conversation_history) > 1:
            recent_messages = conversation_history[-6:]
            history_context = "\n\nRecent conversation context:\n"
            for msg in recent_messages[:-1]:
                role = "User" if msg["role"] == "user" else "Assistant"
                content = msg.get('content', '')[:150]
                history_context += f"{role}: {content}{'...' if len(msg.get('content', '')) > 150 else ''}\n"
        
        full_prompt = f"{emotion_context}{history_context}\n\nUser's current message: {user_message}\n\nYour response:"
        
        try:
            response = gemini_model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=1024,
                )
            )
            if response and hasattr(response, 'text') and response.text:
                return response.text
            else:
                return "I apologize, but I couldn't generate a proper response. Please try again."
        except Exception as gen_error:
            st.warning(f"Generation error: {gen_error}")
            try:
                simple_response = gemini_model.generate_content(f"Please respond to: {user_message}")
                return simple_response.text if simple_response and hasattr(simple_response, 'text') and simple_response.text else "I'm having trouble responding right now. Please try again."
            except:
                return "I'm having trouble responding right now. Please try again."
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "I apologize, but I encountered an error while generating a response. Please try again."

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            st.warning(f"Could not load chat history: {e}")
            backup_name = f"chat_history_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            try:
                os.rename(CHAT_HISTORY_FILE, backup_name)
                st.info(f"Corrupted history backed up as {backup_name}")
            except Exception:
                pass
            return {}
    return {}

def save_chat_history(history):
    try:
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Could not save chat history: {e}")

def create_new_chat():
    chat_id = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    return chat_id

def get_chat_title(messages):
    if messages:
        first_message = messages[0].get('content', '')
        return first_message[:30] + "..." if len(first_message) > 30 else first_message
    return "New Chat"