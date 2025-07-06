"""
Service for handling Groq API interactions.
"""

import os
from templates.prompts import get_history_prompt
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from utils.config import MODEL_CONFIG

class GroqService:
    """Service class for interacting with the Groq API."""
    
    def __init__(self, api_key):
        """
        Initialize the Groq service.
        
        Args:
            api_key (str): Groq API key
        """
        self.api_key = api_key
        self.llm = self._initialize_llm()
        self.chain = self._initialize_chain()
    
    def _initialize_llm(self):
        """Initialize the Groq language model."""
        os.environ['GROQ_API_KEY'] = self.api_key
        return ChatGroq(
            model_name=MODEL_CONFIG["model_name"],
            temperature=MODEL_CONFIG["temperature"],
            max_tokens=MODEL_CONFIG["max_tokens"]
        )
    
    def _initialize_chain(self):
        """Initialize the LLM chain with the history prompt."""
        prompt = self._get_history_prompt()
        return LLMChain(llm=self.llm, prompt=prompt)
    
    def _get_history_prompt(self):
        """
        Returns the chat prompt template for history questions.
        
        Returns:
            ChatPromptTemplate: Configured prompt template
        """
        return get_history_prompt()
    
    def ask_question(self, question):
        """
        Ask a question to the history assistant.
        
        Args:
            question (str): The question to ask
            
        Returns:
            str: The assistant's response
        """
        try:
            response = self.chain.invoke({"question": question})
            return response['text']
        except Exception as e:
            return f"I apologize, but I encountered an error while processing your question: {str(e)}"