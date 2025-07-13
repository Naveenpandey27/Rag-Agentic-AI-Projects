import streamlit as st
import json
import requests
import datetime
from typing import Literal
from config import SOURCE_TYPES, BACKEND_URL

# Custom CSS for enhanced styling
def load_custom_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Topic cards */
    .topic-card {
        background: white;
        border: 1px solid #e1e8ed;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .topic-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .topic-number {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 50%;
        width: 24px;
        height: 24px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.8rem;
        margin-right: 0.5rem;
    }
    
    /* Sidebar styling */
    .sidebar-header {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .settings-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.75rem 2rem;
        font-size: 1rem;
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        border: 1px solid #e1e8ed;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Summary styling */
    .summary-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .summary-text {
        font-size: 1.1rem;
        line-height: 1.8;
        color: #2c3e50;
    }
    
    /* Alert styling */
    .custom-alert {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    
    .alert-success {
        background: #d4edda;
        border-left-color: #28a745;
        color: #155724;
    }
    
    .alert-error {
        background: #f8d7da;
        border-left-color: #dc3545;
        color: #721c24;
    }
    
    .alert-warning {
        background: #fff3cd;
        border-left-color: #ffc107;
        color: #856404;
    }
    
    /* Instructions styling */
    .instructions-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .instructions-card h4 {
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    .instructions-card ol {
        color: #34495e;
        line-height: 1.6;
    }
    
    /* Loading animation */
    .loading-container {
        text-align: center;
        padding: 2rem;
    }
    
    .spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #667eea;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def main(): 
    st.set_page_config(
        page_title="NewsNinja",
        page_icon="🥷",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_custom_css()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🥷 NewsNinja</h1>
        <p>Your Ultimate News & Reddit Intelligence Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
   
    # Initialize session state
    if 'topics' not in st.session_state:
        st.session_state.topics = []
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    if 'summary_data' not in st.session_state:
        st.session_state.summary_data = None

    # Enhanced sidebar
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2> Control Panel</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="settings-section">', unsafe_allow_html=True)
        st.markdown("#### Data Sources")
        source_type = st.selectbox(
            "Choose your data sources",
            options=["both", "news", "reddit"],
            format_func=lambda x: {
                "both": "🌐 News + Reddit",
                "news": "📰 News Only", 
                "reddit": "💬 Reddit Only"
            }[x],
            help="Select which sources to analyze for your topics"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="instructions-card">
            <h4> How to Use</h4>
            <ol>
                <li><strong>Add Topics:</strong> Enter up to 3 topics you want to analyze</li>
                <li><strong>Select Sources:</strong> Choose your preferred data sources</li>
                <li><strong>Generate Analysis:</strong> Click analyze to get comprehensive insights</li>
                <li><strong>Review Results:</strong> Browse and download your analysis</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Stats section
        if st.session_state.topics or st.session_state.summary_data:
            st.markdown("---")
            st.markdown("#### Session Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Topics", len(st.session_state.topics))
            with col2:
                st.metric("Analyses", 1 if st.session_state.summary_data else 0)

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Topic management section
        st.markdown("## Topic Management")
        
        # Input section
        st.markdown("### Add New Topic")
        topic_col1, topic_col2 = st.columns([4, 1])
        
        with topic_col1:
            new_topic = st.text_input(
                "Enter a topic to analyze",
                key=f"topic_input_{st.session_state.input_key}",
                placeholder="e.g. Artificial Intelligence, Climate Change, Cryptocurrency...",
                help="Enter any topic you want to analyze from news and Reddit"
            )
        
        with topic_col2:
            add_disabled = len(st.session_state.topics) >= 3 or not new_topic.strip()
            if st.button("Add Topic", disabled=add_disabled, type="secondary"):
                if new_topic.strip() and new_topic.strip() not in st.session_state.topics:
                    st.session_state.topics.append(new_topic.strip())
                    st.session_state.input_key += 1
                    st.success(f" Added: {new_topic.strip()}")
                    st.rerun()
        
        # Topic limit indicator
        if len(st.session_state.topics) >= 3:
            st.markdown('<div class="custom-alert alert-warning"> Maximum 3 topics allowed</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="custom-alert alert-success"> You can add {3 - len(st.session_state.topics)} more topic(s)</div>', unsafe_allow_html=True)

    with col2:
        # Quick stats
        st.markdown("### Quick Stats")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.topics)}/3</div>
            <div class="metric-label">Topics Added</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{source_type.title()}</div>
            <div class="metric-label">Source Mode</div>
        </div>
        """, unsafe_allow_html=True)

    # Display selected topics with enhanced styling
    if st.session_state.topics:
        st.markdown("---")
        st.markdown("## Selected Topics")
        
        for i, topic in enumerate(st.session_state.topics):
            cols = st.columns([6, 1])
            with cols[0]:
                st.markdown(f"""
                <div class="topic-card">
                    <span class="topic-number">{i+1}</span>
                    <strong>{topic}</strong>
                </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                if st.button("Remove", key=f"remove_{i}", help=f"Remove '{topic}'"):
                    del st.session_state.topics[i]
                    st.session_state.summary_data = None
                    st.success(f"🗑️ Removed: {topic}")
                    st.rerun()

    # Analysis section
    st.markdown("---")
    st.markdown("## Generate Analysis")

    analysis_col1, analysis_col2, analysis_col3 = st.columns([2, 1, 1])
    
    with analysis_col1:
        analyze_button = st.button(
            "🔍 Analyze Topics", 
            disabled=len(st.session_state.topics) == 0,
            type="primary",
            help="Generate comprehensive analysis of your selected topics"
        )
    
    with analysis_col2:
        if st.session_state.summary_data:
            if st.button("🗑️ Clear Results", type="secondary"):
                st.session_state.summary_data = None
                st.success("🗑️ Results cleared!")
                st.rerun()
    
    with analysis_col3:
        if st.session_state.topics:
            st.markdown(f"**Ready to analyze {len(st.session_state.topics)} topic(s)**")

    # Generate summary with enhanced feedback
    if analyze_button:
        if not st.session_state.topics:
            st.markdown('<div class="custom-alert alert-error"> Please add at least one topic before analyzing</div>', unsafe_allow_html=True)
        else:
            # Enhanced loading UI
            with st.spinner(""):
                st.markdown("""
                <div class="loading-container">
                    <div class="spinner"></div>
                    <h3>Analyzing Your Topics...</h3>
                    <p>This may take a few moments while we gather and process data from multiple sources.</p>
                </div>
                """, unsafe_allow_html=True)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Simulate progress updates
                    for i in range(100):
                        progress_bar.progress(i + 1)
                        if i < 30:
                            status_text.text("🔍 Searching news sources...")
                        elif i < 60:
                            status_text.text("💬 Analyzing Reddit discussions...")
                        elif i < 90:
                            status_text.text("🧠 Generating insights...")
                        else:
                            status_text.text("📊 Finalizing analysis...")
                    
                    response = requests.post(
                        f"{BACKEND_URL}/generate-news-summary",
                        json={
                            "topics": st.session_state.topics,
                            "source_type": source_type
                        },
                        timeout=120
                    )

                    if response.status_code == 200:
                        st.session_state.summary_data = response.json()
                        st.markdown('<div class="custom-alert alert-success"> Analysis completed successfully!</div>', unsafe_allow_html=True)
                        st.balloons()
                        st.rerun()
                    else:
                        handle_api_error(response)

                except requests.exceptions.ConnectionError:
                    st.markdown('<div class="custom-alert alert-error"> Connection Error: Could not reach the backend server. Please ensure the backend is running.</div>', unsafe_allow_html=True)
                except requests.exceptions.Timeout:
                    st.markdown('<div class="custom-alert alert-error"> Request timed out. The analysis is taking longer than expected.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="custom-alert alert-error"> Unexpected Error: {str(e)}</div>', unsafe_allow_html=True)

    # Display results with enhanced styling
    if st.session_state.summary_data:
        display_summary_results(st.session_state.summary_data)


def display_summary_results(summary_data):
    """Display the structured summary results with enhanced styling"""
    st.markdown("---")
    st.markdown("# Analysis Results")
    
    # Enhanced metadata display
    with st.expander(" Analysis Details", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(summary_data.get("topics", []))}</div>
                <div class="metric-label">Topics Analyzed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{summary_data.get("source_type", "").title()}</div>
                <div class="metric-label">Sources Used</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            timestamp = summary_data.get("timestamp", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">📅</div>
                <div class="metric-label">{timestamp}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            word_count = len(summary_data.get("summary", "").split())
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{word_count}</div>
                <div class="metric-label">Words Generated</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Enhanced summary display
    if "summary" in summary_data:
        st.markdown("## Comprehensive Summary")
        
        # Clean and format the summary content
        summary_content = summary_data["summary"]
        
        # Clean up the content by removing markdown formatting
        import re
        
        # Remove bold markdown (**text**)
        summary_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', summary_content)
        
        # Remove italic markdown (*text*)
        summary_content = re.sub(r'(?<!\*)\*(?!\*)([^*]+)\*(?!\*)', r'<em>\1</em>', summary_content)
        
        # Process bullet points
        summary_content = re.sub(r'^\* ', '• ', summary_content, flags=re.MULTILINE)
        
        # Split into lines and process
        lines = summary_content.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('# '):
                # Convert to HTML header
                processed_lines.append(f"<h2 style='color: #2c3e50; margin-top: 2rem; margin-bottom: 1rem; font-weight: 700;'>{line[2:]}</h2>")
            elif line.startswith('## '):
                # Convert to HTML subheader
                processed_lines.append(f"<h3 style='color: #34495e; margin-top: 1.5rem; margin-bottom: 0.8rem; font-weight: 600;'>{line[3:]}</h3>")
            elif line.startswith('### '):
                # Convert to HTML sub-subheader
                processed_lines.append(f"<h4 style='color: #5a6c7d; margin-top: 1rem; margin-bottom: 0.5rem; font-weight: 500;'>{line[4:]}</h4>")
            elif line.startswith('• '):
                # Bullet point
                processed_lines.append(f"<div style='margin-left: 1rem; margin-bottom: 0.5rem; line-height: 1.6;'><span style='color: #667eea; font-weight: bold;'>•</span> {line[2:]}</div>")
            elif line and not line.startswith('#'):
                # Regular paragraph
                if line:  # Only add non-empty lines
                    processed_lines.append(f"<p style='margin-bottom: 1rem; line-height: 1.8; text-align: justify;'>{line}</p>")
        
        formatted_summary = ''.join(processed_lines)
        
        # If no specific formatting was found, process as clean paragraphs
        if not formatted_summary.strip():
            paragraphs = summary_content.split('\n\n')
            formatted_summary = ''.join([f"<p style='margin-bottom: 1rem; line-height: 1.8; text-align: justify;'>{p.strip()}</p>" for p in paragraphs if p.strip()])
        
        st.markdown(f"""
        <div class="summary-container">
            <div class="summary-text">{formatted_summary}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced download section
    st.markdown("---")
    st.markdown("## Export Your Analysis")
    
    download_col1, download_col2, download_col3 = st.columns([2, 1, 1])
    
    with download_col1:
        st.markdown("Download your analysis in JSON format for future reference or sharing.")
    
    with download_col2:
        timestamp = summary_data.get('timestamp', datetime.datetime.now().strftime("%Y%m%d_%H%M"))
        filename = f"newsninja_analysis_{timestamp}.json"
        
        if st.download_button(
            " Download JSON",
            data=json.dumps(summary_data, indent=2),
            file_name=filename,
            mime="application/json",
            type="primary"
        ):
            st.success("Analysis downloaded successfully!")
    
    with download_col3:
        # Generate text version for download
        text_content = f"""
NewsNinja Analysis Report
========================

Generated: {summary_data.get('timestamp', 'N/A')}
Topics: {', '.join(summary_data.get('topics', []))}
Sources: {summary_data.get('source_type', 'N/A')}

Summary:
{summary_data.get('summary', 'N/A')}
        """
        
        if st.download_button(
            "Download Text",
            data=text_content,
            file_name=f"newsninja_analysis_{timestamp}.txt",
            mime="text/plain",
            type="secondary"
        ):
            st.success("Text version downloaded!")


def handle_api_error(response):
    """Handle API error responses with enhanced styling"""
    try:
        error_detail = response.json().get("detail", "Unknown error")
        st.markdown(f'<div class="custom-alert alert-error"> API Error ({response.status_code}): {error_detail}</div>', unsafe_allow_html=True)
    except ValueError:
        st.markdown(f'<div class="custom-alert alert-error"> Unexpected API Response: {response.text}</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()