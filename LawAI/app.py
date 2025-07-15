import streamlit as st
import logging
from models.vector_db import PDFProcessor
from src.config.logging_config import configure_logging
from utils.style_utils import load_css
load_css()

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="AI Lawyer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'pdf_processor' not in st.session_state:
    st.session_state.pdf_processor = None
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None
if 'pdf_processed' not in st.session_state:
    st.session_state.pdf_processed = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_pdf_name' not in st.session_state:
    st.session_state.current_pdf_name = None

# Title and description
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.markdown('<h1 class="centered-title"> LawAI</h1>', unsafe_allow_html=True)
st.markdown('<p class="centered-subtitle">Upload your PDF document and ask questions about it using AI!</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header(" Configuration")
    groq_api_key = st.text_input(
        "Groq API Key:",
        type="password",
        help="Get your free API key from https://console.groq.com/keys"
    )
    
    if groq_api_key:
        st.success(" API Key provided!")
    else:
        st.info(" Enter your Groq API key")
    
    st.markdown("---")
    uploaded_file = st.file_uploader(" Upload PDF", type="pdf", accept_multiple_files=False)
    
    if uploaded_file:
        st.success(f" {uploaded_file.name}")
        
        if st.button(" Process PDF", disabled=not groq_api_key, use_container_width=True):
            if groq_api_key:
                try:
                    with st.spinner(" Initializing AI system..."):
                        processor = PDFProcessor(groq_api_key)
                    
                    qa_chain, num_pages, num_chunks = processor.process_pdf_and_create_qa(uploaded_file)
                    
                    st.session_state.pdf_processor = processor
                    st.session_state.qa_chain = qa_chain
                    st.session_state.pdf_processed = True
                    st.session_state.current_pdf_name = uploaded_file.name
                    st.session_state.chat_history = []
                    
                    st.success(f"Processing Complete!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Pages", num_pages)
                    with col2:
                        st.metric(" Chunks", num_chunks)
                    
                    st.info("🎉 Ready to answer questions about your document!")
                    
                except Exception as e:
                    st.error(f" Processing Error: {str(e)}")
                    logger.error(f"PDF processing error: {str(e)}")
                    st.session_state.pdf_processed = False
                    st.session_state.pdf_processor = None
                    st.session_state.qa_chain = None
            else:
                st.error("Please enter your API key first!")
    
    if st.session_state.pdf_processed:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        with col2:
            if st.button("New PDF", use_container_width=True):
                st.session_state.pdf_processed = False
                st.session_state.pdf_processor = None
                st.session_state.qa_chain = None
                st.session_state.chat_history = []
                st.session_state.current_pdf_name = None
                st.rerun()
    
    if st.session_state.pdf_processed and st.session_state.current_pdf_name:
        st.markdown("---")
        st.markdown("**Current Document:**")
        st.markdown(f" {st.session_state.current_pdf_name}")
        
        if st.session_state.pdf_processor:
            try:
                doc_info = st.session_state.pdf_processor.get_document_info()
                if doc_info.get("status") == "Documents loaded":
                    st.markdown(f" **Stats:** {doc_info.get('total_chunks', 'N/A')} chunks")
            except Exception as e:
                logger.error(f"Error getting document info: {str(e)}")

# Main content area
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    if not groq_api_key:
        st.markdown("### Get Started")
        st.warning("Please enter your Groq API key in the sidebar to get started.")
    elif not uploaded_file:
        st.markdown("### Upload Your Document")
        st.info("Please upload a PDF document in the sidebar to begin.")
    elif not st.session_state.pdf_processed:
        st.markdown("### Ready to Process")
        st.info("Click 'Process PDF' in the sidebar to analyze your document.")
    else:
        st.markdown("### Chat with your PDF")
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        user_query = st.chat_input("Ask a question about your PDF...")
        
        if user_query:
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_query
            })
            
            with st.chat_message("user"):
                st.markdown(user_query)
            
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.pdf_processor.answer_query(user_query)
                        st.markdown(response)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": response
                        })
                    except Exception as e:
                        error_message = f"Sorry, I encountered an error: {str(e)}"
                        st.error(error_message)
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": error_message
                        })

# Footer
st.markdown("---")
with st.columns([1, 6, 1])[1]:
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
        "Built with using Streamlit, LangChain, and Groq"
        "</div>", 
        unsafe_allow_html=True
    )