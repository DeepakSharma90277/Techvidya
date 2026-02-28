"""
Configuration Management
Handles environment variables and application settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration class"""
    
    # API Keys
    TAVILY_API_KEY = os.getenv('TAVILY_API_KEY', '')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # Backend API Configuration
    BACKEND_BASE_URL = os.getenv('BACKEND_BASE_URL', 'http://localhost:4000/api/v1')
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'groq')  # 'groq' or 'ollama'
    LLM_MODEL = os.getenv('LLM_MODEL', 'llama-3.1-8b-instant')  # Groq model - fast and stable
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.7'))
    LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', '1024'))
    
    # Tavily Configuration
    TAVILY_SEARCH_DEPTH = os.getenv('TAVILY_SEARCH_DEPTH', 'advanced')  # 'basic' or 'advanced'
    TAVILY_MAX_RESULTS = int(os.getenv('TAVILY_MAX_RESULTS', '5'))
    
    # Application Settings
    MAX_CHAT_HISTORY = int(os.getenv('MAX_CHAT_HISTORY', '50'))
    RECOMMENDATIONS_LIMIT = int(os.getenv('RECOMMENDATIONS_LIMIT', '10'))
    
    # Assessment Categories
    ASSESSMENT_CATEGORIES = [
        'Programming',
        'Data Structures & Algorithms',
        'Web Development',
        'Database Management',
        'Machine Learning',
        'Cloud Computing',
        'Cybersecurity',
        'Mobile Development',
        'DevOps',
        'Software Engineering'
    ]
    
    # Difficulty Levels
    DIFFICULTY_LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert']
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        errors = []
        
        if not cls.TAVILY_API_KEY:
            errors.append("TAVILY_API_KEY is not set")
        
        if cls.LLM_PROVIDER == 'groq' and not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY is not set (required when using Groq provider)")
        
        return errors
    
    @classmethod
    def get_config_summary(cls):
        """Get a summary of current configuration"""
        return {
            'llm_provider': cls.LLM_PROVIDER,
            'llm_model': cls.LLM_MODEL,
            'backend_url': cls.BACKEND_BASE_URL,
            'tavily_configured': bool(cls.TAVILY_API_KEY),
            'groq_configured': bool(cls.GROQ_API_KEY),
        }
