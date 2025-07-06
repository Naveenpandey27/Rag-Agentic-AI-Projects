"""
Configuration and constants for the History Assistant application.
"""

PAGE_CONFIG = {
    "page_title": "History Assistant - Powered by Groq",
    "page_icon": "🏛️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Model configuration
MODEL_CONFIG = {
    "model_name": "llama-3.3-70b-versatile",
    "temperature": 0.1,
    "max_tokens": 4000
}

# Default messages
DEFAULT_MESSAGES = [
    {
        "role": "assistant",
        "content": "👋 Welcome! I'm your History Teacher powered by Groq. I'm here to help you explore the fascinating world of history. Feel free to ask me about any historical period, event, figure, or civilization!"
    }
]