"""
Author: Naveen Pandey
Date: 06/07/2025

"""

import os
import sys

# === Ensure root directory is in sys.path for module resolution ===
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_path not in sys.path:
    sys.path.append(root_path)

import streamlit as st
from utils.config import PAGE_CONFIG
from utils.styles import load_css
from services.chat_service import ChatService
from utils.helpers import get_history_topics

def initialize_session_state():
    """Initialize the Streamlit session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        st.session_state.add_welcome_message = True

def render_sidebar():
    """Render the sidebar UI components."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input(
            "Enter your Groq API Key:",
            type="password",
            placeholder="gsk_...",
            help="Get your API key from https://console.groq.com"
        )
        
        st.divider()
        render_suggested_topics()
        st.divider()
        
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
    return api_key

def render_suggested_topics():
    """Render the suggested topics section in the sidebar."""
    st.header("💡 Suggested Topics")
    topics = get_history_topics()
    
    for topic in topics:
        if st.button(topic, key=f"topic_{topic}", use_container_width=True):
            topic_name = topic.split(" ", 1)[1] if " " in topic else topic
            st.session_state.selected_topic = f"Tell me about {topic_name}"

def render_main_content(api_key):
    """Render the main chat interface."""
    # Header
    st.markdown('<h1 class="main-header">🏛️ History Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Explore the fascinating world of history with AI-powered insights</p>', unsafe_allow_html=True)
    
    # Check for API key
    if not api_key:
        st.warning("🔑 Please enter your Groq API Key in the sidebar to start chatting!")
        return
    
    # Initialize chat service
    chat_service = ChatService(api_key)
    
    # Display chat messages
    chat_service.display_chat_messages()
    
    # Handle selected topic from sidebar
    chat_service.handle_selected_topic()
    
    # Handle user input
    chat_service.handle_user_input()
    
    # Render features section
    render_features()

def render_features():
    """Render the features section at the bottom of the page."""
    st.divider()
    st.header("✨ Features")
    
    col1, col2, col3 = st.columns(3)
    
    features = [
        {
            "title": "🤖 AI-Powered",
            "description": "Powered by Groq's Mixtral-8x7b model for accurate and engaging historical insights"
        },
        {
            "title": "🌍 Comprehensive Coverage",
            "description": "Explore history from ancient civilizations to modern times across all cultures"
        },
        {
            "title": "💡 Interactive Learning",
            "description": "Engaging conversations that make history come alive with context and storytelling"
        }
    ]
    
    for i, feature in enumerate(features):
        with [col1, col2, col3][i]:
            st.markdown(f"""
            <div class="feature-card">
                <h4>{feature['title']}</h4>
                <p>{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)

def main():
    """Main function to run the History Assistant application."""
    # Configure page settings
    st.set_page_config(**PAGE_CONFIG)
    
    # Load CSS styles
    load_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get API key
    api_key = render_sidebar()
    
    # Render main content
    render_main_content(api_key)

if __name__ == "__main__":
    main()