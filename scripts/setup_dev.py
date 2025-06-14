#!/usr/bin/env python3
"""
Development environment setup script for Dudil Mental Health AI
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import shutil

class DevelopmentSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.venv_path = self.project_root / "venv"
        
    def run(self):
        """Run complete development setup"""
        print("🧠 Dudil Mental Health AI - Development Setup")
        print("=" * 50)
        
        # Check Python version
        self.check_python_version()
        
        # Create virtual environment
        self.create_virtual_environment()
        
        # Install dependencies
        self.install_dependencies()
        
        # Create directory structure
        self.create_directories()
        
        # Copy configuration files
        self.setup_configuration()
        
        # Download models
        self.download_models()
        
        # Setup database
        self.setup_database()
        
        # Create test data
        self.create_test_data()
        
        # Run initial tests
        self.run_tests()
        
        print("\n✅ Setup complete!")
        print("\n📝 Next steps:")
        print("1. Edit .env file with your API keys")
        print("2. Run 'make run' to start the application")
        print("3. Visit http://localhost:8501")
        
    def check_python_version(self):
        """Ensure Python 3.8+ is being used"""
        print("\n📍 Checking Python version...")
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8+ is required")
            sys.exit(1)
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        
    def create_virtual_environment(self):
        """Create virtual environment if it doesn't exist"""
        print("\n📍 Setting up virtual environment...")
        
        if not self.venv_path.exists():
            subprocess.run([sys.executable, "-m", "venv", "venv"])
            print("✅ Virtual environment created")
        else:
            print("✅ Virtual environment already exists")
            
        # Activate instructions
        if sys.platform == "win32":
            activate_cmd = "venv\\Scripts\\activate"
        else:
            activate_cmd = "source venv/bin/activate"
            
        print(f"   Run '{activate_cmd}' to activate")
        
    def install_dependencies(self):
        """Install all required dependencies"""
        print("\n📍 Installing dependencies...")
        
        # Upgrade pip
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install production requirements
        if (self.project_root / "requirements.txt").exists():
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ])
            print("✅ Production dependencies installed")
        
        # Install development requirements
        if (self.project_root / "requirements-dev.txt").exists():
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"
            ])
            print("✅ Development dependencies installed")
            
    def create_directories(self):
        """Create necessary directory structure"""
        print("\n📍 Creating directory structure...")
        
        directories = [
            "src/core",
            "src/models",
            "src/ai",
            "src/ui/layouts",
            "src/ui/components",
            "src/ui/pages",
            "src/services",
            "src/data/database/migrations",
            "src/data/storage",
            "src/data/cache",
            "src/utils",
            "tests/unit",
            "tests/integration",
            "tests/fixtures",
            "docs/api",
            "docs/user_guide",
            "docs/developer_guide",
            "scripts",
            "resources/models",
            "resources/assets/images",
            "resources/assets/sounds",
            "resources/data",
            "deployment/docker",
            "deployment/kubernetes",
            "config/prompts",
            "logs",
            "data/uploads",
            "data/exports"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py for Python packages
            if directory.startswith("src/") or directory.startswith("tests/"):
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.touch()
                    
        print("✅ Directory structure created")
        
    def setup_configuration(self):
        """Setup configuration files"""
        print("\n📍 Setting up configuration...")
        
        # Copy .env.example to .env if it doesn't exist
        env_example = self.project_root / ".env.example"
        env_file = self.project_root / ".env"
        
        if env_example.exists() and not env_file.exists():
            shutil.copy(env_example, env_file)
            print("✅ Created .env from .env.example")
        
        # Create .env.example if it doesn't exist
        if not env_example.exists():
            env_content = """# Dudil Mental Health AI Configuration

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro

# Model Configuration
EMOTION_MODEL=j-hartmann/emotion-english-distilroberta-base
DEPRESSION_MODEL=paulagarciaserrano/roberta-depression-detection
WHISPER_MODEL=base

# Database
DATABASE_URL=sqlite:///data/dudil.db
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Features
ENABLE_VOICE_INPUT=true
ENABLE_AI_THERAPIST=true
ENABLE_MOOD_PREDICTION=true
ENABLE_CRISIS_DETECTION=true

# Analytics
ENABLE_ANALYTICS=true
ANALYTICS_KEY=

# Storage
UPLOAD_FOLDER=data/uploads
EXPORT_FOLDER=data/exports
MAX_UPLOAD_SIZE=10485760

# Session
SESSION_TIMEOUT=3600
MAX_SESSIONS_PER_USER=5

# Development
DEBUG=true
LOG_LEVEL=INFO
"""
            with open(env_example, 'w', encoding="utf-8") as f:
                f.write(env_content)
            print("✅ Created .env.example")
            
        # Create config files
        self.create_config_files()
        
    def create_config_files(self):
        """Create necessary configuration files"""
        
        # Create .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
htmlcov/
*.egg-info/
dist/
build/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
data/
logs/
resources/models/
*.db
*.log
chat_history.json

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/secrets.toml
"""
        gitignore_path = self.project_root / ".gitignore"
        if not gitignore_path.exists():
            with open(gitignore_path, 'w', encoding="utf-8") as f:
                f.write(gitignore_content)
            print("✅ Created .gitignore")
            
        # Create .streamlit/config.toml
        streamlit_dir = self.project_root / ".streamlit"
        streamlit_dir.mkdir(exist_ok=True)
        
        streamlit_config = """[theme]
primaryColor = "#7B68EE"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 10

[browser]
gatherUsageStats = false
"""
        config_path = streamlit_dir / "config.toml"
        if not config_path.exists():
            with open(config_path, 'w', encoding="utf-8") as f:
                f.write(streamlit_config)
            print("✅ Created Streamlit config")
            
        # Create crisis resources JSON
        crisis_resources = {
            "global": {
                "name": "International Crisis Resources",
                "resources": [
                    {
                        "name": "Crisis Text Line",
                        "description": "Text support for crisis situations",
                        "contact": "Text HOME to 741741",
                        "available": "24/7",
                        "languages": ["English"]
                    }
                ]
            },
            "US": {
                "name": "United States",
                "resources": [
                    {
                        "name": "988 Suicide & Crisis Lifeline",
                        "description": "24/7 crisis support",
                        "contact": "988",
                        "available": "24/7",
                        "languages": ["English", "Spanish"]
                    },
                    {
                        "name": "Crisis Text Line",
                        "contact": "Text HOME to 741741",
                        "available": "24/7"
                    },
                    {
                        "name": "SAMHSA National Helpline",
                        "contact": "1-800-662-4357",
                        "available": "24/7"
                    }
                ]
            },
            "UK": {
                "name": "United Kingdom",
                "resources": [
                    {
                        "name": "Samaritans",
                        "contact": "116 123",
                        "available": "24/7"
                    },
                    {
                        "name": "Crisis Text Line UK",
                        "contact": "Text SHOUT to 85258",
                        "available": "24/7"
                    }
                ]
            }
        }
        
        resources_path = self.project_root / "resources/data/crisis_resources.json"
        with open(resources_path, 'w', encoding="utf-8") as f:
            json.dump(crisis_resources, f, indent=2)
        print("✅ Created crisis resources")
        
        # Create linguistic markers
        markers = {
            "depression": {
                "cognitive": {
                    "absolutist": ["always", "never", "nothing", "everything", "completely"],
                    "hopelessness": ["no point", "give up", "worthless", "cant go on", "meaningless"],
                    "negative_self": ["im stupid", "i fail", "my fault", "hate myself", "loser"]
                },
                "behavioral": {
                    "social_withdrawal": ["alone", "nobody understands", "isolate", "withdrawn"],
                    "sleep_issues": ["cant sleep", "insomnia", "tired all time", "exhausted"],
                    "appetite": ["not eating", "no appetite", "overeating", "lost weight"]
                }
            },
            "anxiety": {
                "cognitive": {
                    "worry": ["what if", "worried about", "anxious", "nervous", "concerned"],
                    "catastrophizing": ["worst case", "disaster", "terrible", "awful"],
                    "rumination": ["cant stop thinking", "obsessing", "overthinking"]
                },
                "physical": {
                    "panic": ["heart racing", "cant breathe", "chest tight", "dizzy"],
                    "tension": ["on edge", "cant relax", "restless", "tense"]
                }
            },
            "crisis": {
                "suicidal": ["kill myself", "end it all", "suicide", "not worth living"],
                "self_harm": ["hurt myself", "cut myself", "self harm", "punish myself"],
                "danger": ["goodbye", "sorry for everything", "final decision"]
            }
        }
        
        markers_path = self.project_root / "resources/data/markers.json"
        with open(markers_path, 'w', encoding="utf-8") as f:
            json.dump(markers, f, indent=2)
        print("✅ Created linguistic markers")
        
    def download_models(self):
        """Download required models"""
        print("\n📍 Downloading models...")
        
        # Create model download script if it doesn't exist
        download_script = self.project_root / "scripts/download_models.py"
        if not download_script.exists():
            script_content = '''#!/usr/bin/env python3
"""Download required models for Dudil Mental Health AI"""

import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import whisper
import nltk

def download_models():
    """Download all required models"""
    print("Downloading models...")
    
    # Create models directory
    models_dir = "resources/models"
    os.makedirs(models_dir, exist_ok=True)
    
    # Download emotion model
    print("📥 Downloading emotion detection model...")
    emotion_model = "j-hartmann/emotion-english-distilroberta-base"
    pipeline("text-classification", model=emotion_model)
    
    # Download NLTK data
    print("📥 Downloading NLTK data...")
    nltk_data = ['punkt', 'stopwords', 'vader_lexicon']
    for dataset in nltk_data:
        try:
            nltk.download(dataset, quiet=True)
        except:
            pass
    
    # Note about Whisper model
    print("ℹ️  Whisper model will be downloaded on first use")
    
    print("✅ Model download complete!")

if __name__ == "__main__":
    download_models()
'''
            with open(download_script, 'w', encoding="utf-8") as f:
                f.write(script_content)
            os.chmod(download_script, 0o755)
        
        # Run the download script
        subprocess.run([sys.executable, str(download_script)])
        
    def setup_database(self):
        """Setup database"""
        print("\n📍 Setting up database...")
        
        # Create database migration script
        migrate_script = self.project_root / "scripts/migrate_db.py"
        if not migrate_script.exists():
            script_content = '''#!/usr/bin/env python3
"""Database migration script"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from src.data.database.models import Base

def migrate():
    """Run database migrations"""
    print("Running database migrations...")
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL", "sqlite:///data/dudil.db")
    
    # Create data directory if it doesn't exist
    if database_url.startswith("sqlite"):
        os.makedirs("data", exist_ok=True)
    
    # Create engine and tables
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    
    print("✅ Database migrations complete!")

if __name__ == "__main__":
    migrate()
'''
            with open(migrate_script, 'w', encoding="utf-8") as f:
                f.write(script_content)
            os.chmod(migrate_script, 0o755)
        
        # Note: Don't run migration here as models may not be set up yet
        print("✅ Database setup script created")
        
    def create_test_data(self):
        """Create test data for development"""
        print("\n📍 Creating test data...")
        
        # Create sample test fixtures
        fixtures_dir = self.project_root / "tests/fixtures"
        test_data_file = fixtures_dir / "test_data.py"
        
        if not test_data_file.exists():
            test_content = '''"""Test data fixtures for Dudil Mental Health AI"""

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
'''
            with open(test_data_file, 'w', encoding="utf-8") as f:
                f.write(test_content)
                
        print("✅ Test data created")
        
    def run_tests(self):
        """Run initial tests to verify setup"""
        print("\n📍 Running initial tests...")
        
        # Create a simple test file
        test_file = self.project_root / "tests/test_setup.py"
        if not test_file.exists():
            test_content = '''"""Basic setup tests"""

def test_imports():
    """Test that basic imports work"""
    try:
        import streamlit
        import google.generativeai
        import transformers
        import numpy
        import pandas
        assert True
    except ImportError as e:
        assert False, f"Import failed: {e}"

def test_environment():
    """Test environment setup"""
    import os
    assert os.path.exists(".env") or os.path.exists(".env.example")
'''
            with open(test_file, 'w', encoding="utf-8") as f:
                f.write(test_content)
        
        # Run the test
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_setup.py", "-v"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Initial tests passed")
        else:
            print("⚠️  Some tests failed (this is okay for initial setup)")
            

if __name__ == "__main__":
    setup = DevelopmentSetup()
    setup.run()