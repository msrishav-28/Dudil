"""Test data fixtures for Dudil Mental Health AI"""

# Sample messages for testing
SAMPLE_MESSAGES = [
    {
        "text": "I've been feeling really anxious about work lately",
        "expected_emotion": "fear",
        "expected_risk": "low"
    },
    {
        "text": "I'm so happy today! Everything is going great!",
        "expected_emotion": "joy",
        "expected_risk": "minimal"
    },
    {
        "text": "I can't sleep and nothing seems to help anymore",
        "expected_emotion": "sadness",
        "expected_risk": "moderate"
    }
]

# Sample user profiles
TEST_USERS = [
    {
        "id": "test_user_1",
        "name": "Test User 1",
        "settings": {
            "notifications": True,
            "anonymous_mode": False
        }
    }
]

# Sample audio data for voice testing
SAMPLE_AUDIO_PARAMS = {
    "duration": 5.0,
    "sample_rate": 16000,
    "channels": 1
}
