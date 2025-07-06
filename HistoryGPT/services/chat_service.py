"""
Service for handling chat functionality in the History Assistant application.
"""

import streamlit as st
from services.groq_service import GroqService
from utils.config import DEFAULT_MESSAGES

class ChatService:
    """Service class for handling chat functionality."""
    
    def __init__(self, api_key):
        """
        Initialize the chat service.
        
        Args:
            api_key (str): Groq API key
        """
        self.api_key = api_key
        self.groq_service = GroqService(api_key)
        
        # Add welcome message if this is the first run
        if 'messages' not in st.session_state or len(st.session_state.messages) == 0:
            st.session_state.messages = DEFAULT_MESSAGES.copy()
    
    def display_chat_messages(self):
        """Display all chat messages in the UI."""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def handle_selected_topic(self):
        """
        Handle a topic selected from the sidebar.
        Adds the topic as a user message and generates a response.
        """
        if 'selected_topic' in st.session_state:
            user_input = st.session_state.selected_topic
            del st.session_state.selected_topic
            
            # Add user message
            self._add_user_message(user_input)
            
            # Generate and display assistant response
            self._generate_assistant_response(user_input)
            
            st.rerun()
    
    def handle_user_input(self):
        """
        Handle user input from the chat interface.
        """
        if prompt := st.chat_input("Ask me anything about history..."):
            # Add user message
            self._add_user_message(prompt)
            
            # Generate and display assistant response
            self._generate_assistant_response(prompt)
    
    def _add_user_message(self, content):
        """Add a user message to the chat history."""
        st.session_state.messages.append({"role": "user", "content": content})
        with st.chat_message("user"):
            st.markdown(content)
    
    def _generate_assistant_response(self, prompt):
        """Generate and display an assistant response to the given prompt."""
        with st.chat_message("assistant"):
            with st.spinner("🔍 Researching your question..."):
                response = self.groq_service.ask_question(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})