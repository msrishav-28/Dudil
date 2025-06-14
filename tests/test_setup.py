"""Basic setup tests"""

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
