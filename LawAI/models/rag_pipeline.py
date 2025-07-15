import logging
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

class RAGPipeline:
    """Enhanced RAG Pipeline for PDF Question Answering"""
    
    def __init__(self, groq_api_key: str, model_name: str = "deepseek-r1-distill-llama-70b"):
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        self.llm = self._initialize_llm()
        self.embeddings = self._initialize_embeddings()
        self.vector_store = None
        self.retriever = None
        self.chain = None
        
    def _initialize_llm(self) -> ChatGroq:
        try:
            return ChatGroq(
                groq_api_key=self.groq_api_key,
                model_name=self.model_name,
                temperature=0.1,
                max_tokens=1024,
                timeout=60
            )
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {str(e)}")
            raise
    
    def _initialize_embeddings(self) -> HuggingFaceEmbeddings:
        try:
            return HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
        except Exception as e:
            logger.error(f"Failed to initialize embeddings: {str(e)}")
            raise
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        try:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
            self.retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
            logger.info(f"Created vector store with {len(documents)} documents")
            return self.vector_store
        except Exception as e:
            logger.error(f"Failed to create vector store: {str(e)}")
            raise
    
    def _get_custom_prompt(self) -> ChatPromptTemplate:
        template = """
        You are an expert AI Legal Assistant. Your role is to provide accurate, helpful legal information based on the provided context.
        
        **Instructions:**
        1. Use ONLY the information provided in the context below to answer questions
        2. If the answer is not found in the context, clearly state "I don't have enough information in the provided document to answer this question"
        3. Provide specific article numbers, sections, or references when available
        4. Structure your response clearly with bullet points or numbered lists when appropriate
        5. Be professional and precise in your language
        6. If multiple articles or sections are relevant, mention all of them
        7. Do not make assumptions or provide information not explicitly stated in the context
        
        **Context:**
        {context}
        
        **Question:** {question}
        
        **Answer:**
        """
        return ChatPromptTemplate.from_template(template)
    
    def _format_docs(self, documents: List[Document]) -> str:
        if not documents:
            return "No relevant information found in the document."
        
        formatted_context = []
        for i, doc in enumerate(documents, 1):
            metadata_info = ""
            if hasattr(doc, 'metadata') and doc.metadata:
                if 'page' in doc.metadata:
                    metadata_info = f" (Page {doc.metadata['page']})"
                elif 'source' in doc.metadata:
                    metadata_info = f" (Source: {doc.metadata['source']})"
            
            formatted_context.append(f"**Excerpt {i}:**{metadata_info}\n{doc.page_content}")
        
        return "\n\n".join(formatted_context)
    
    def setup_chain(self):
        if not self.retriever:
            raise ValueError("Vector store and retriever must be created first")
        
        prompt = self._get_custom_prompt()
        self.chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
    
    def answer_query(self, question: str) -> str:
        if not self.chain:
            raise ValueError("RAG chain not initialized. Setup chain first.")
        
        try:
            question = question.strip()
            if not question:
                return "Please provide a valid question."
            
            # Use invoke method which should handle the response properly
            response = self.chain.invoke(question)
            
            # Ensure we return a string
            if hasattr(response, 'content'):
                return str(response.content)
            else:
                return str(response)
                
        except Exception as e:
            logger.error(f"Error answering query: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def get_document_stats(self) -> Dict[str, Any]:
        if not self.vector_store:
            return {"status": "No documents loaded"}
        
        return {
            "status": "Documents loaded",
            "total_chunks": self.vector_store.index.ntotal,
            "embedding_dimension": self.vector_store.index.d,
            "model_name": self.model_name
        }
    
    def clear_vector_store(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None