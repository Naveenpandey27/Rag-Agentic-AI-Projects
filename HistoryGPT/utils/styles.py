"""
CSS styles and styling utilities for the History Assistant application.
"""
import streamlit as st

MAIN_CSS = """
<style>
    .main-header {
        text-align: center;
        color: #2E4057;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #546E7A;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    
    .user-message {
        background-color: #E3F2FD;
        border-left-color: #2196F3;
    }
    
    .assistant-message {
        background-color: #F3E5F5;
        border-left-color: #9C27B0;
    }
    
    .topic-card {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        margin-bottom: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .topic-card:hover {
        background-color: #E8F5E8;
        border-color: #4CAF50;
    }
    
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .feature-card {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FF9800;
        margin-bottom: 1rem;
    }
</style>
"""

def load_css():
    """Load the custom CSS styles."""
    st.markdown(MAIN_CSS, unsafe_allow_html=True)