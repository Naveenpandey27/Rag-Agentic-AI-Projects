import os
import tempfile
import logging
from typing import List, Tuple
from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from .rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)

class PDFProcessor:
    """PDF processing system with RAG pipeline integration"""
    
    def __init__(self, groq_api_key: str, model_name: str = "deepseek-r1-distill-llama-70b"):
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        self.rag_pipeline = RAGPipeline(groq_api_key, model_name)
        self.current_pdf_name = None
    
    def load_pdf_from_upload(self, uploaded_file) -> List[Document]:
        try:
            self.current_pdf_name = uploaded_file.name
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            loader = PDFPlumberLoader(tmp_file_path)
            documents = loader.load()
            
            for i, doc in enumerate(documents):
                doc.metadata.update({
                    "source": self.current_pdf_name,
                    "page": i + 1,
                    "total_pages": len(documents)
                })
            
            os.unlink(tmp_file_path)
            return documents
            
        except Exception as e:
            logger.error(f"Error loading PDF: {str(e)}")
            raise Exception(f"Failed to load PDF: {str(e)}")
    
    def create_chunks(self, documents: List[Document]) -> List[Document]:
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1200,
                chunk_overlap=300,
                add_start_index=True,
                separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
            )
            
            text_chunks = text_splitter.split_documents(documents)
            
            for i, chunk in enumerate(text_chunks):
                chunk.metadata.update({
                    "chunk_id": i,
                    "total_chunks": len(text_chunks)
                })
            
            return text_chunks
            
        except Exception as e:
            logger.error(f"Error creating chunks: {str(e)}")
            raise Exception(f"Failed to create chunks: {str(e)}")
    
    def process_pdf_and_create_qa(self, uploaded_file) -> Tuple[RAGPipeline, int, int]:
        try:
            documents = self.load_pdf_from_upload(uploaded_file)
            text_chunks = self.create_chunks(documents)
            self.rag_pipeline.create_vector_store(text_chunks)
            self.rag_pipeline.setup_chain()
            return self.rag_pipeline, len(documents), len(text_chunks)
            
        except Exception as e:
            logger.error(f"Error in PDF processing pipeline: {str(e)}")
            raise Exception(f"PDF processing failed: {str(e)}")
    
    def answer_query(self, query: str) -> str:
        try:
            if not self.rag_pipeline.chain:
                raise ValueError("PDF not processed yet. Please process a PDF first.")
            return self.rag_pipeline.answer_query(query)
        except Exception as e:
            logger.error(f"Error answering query: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def get_document_info(self) -> dict:
        info = self.rag_pipeline.get_document_stats()
        if self.current_pdf_name:
            info["pdf_name"] = self.current_pdf_name
        return info
    
    def clear_current_document(self):
        self.rag_pipeline.clear_vector_store()
        self.current_pdf_name = None