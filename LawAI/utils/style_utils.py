import streamlit as st

def load_css():
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            padding: 1rem 0;
            border-bottom: 2px solid #f0f0f0;
            margin-bottom: 2rem;
        }
        .centered-title {
            text-align: center;
            font-size: 3rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        .centered-subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #34495e;
            margin-bottom: 1rem;
        }
        .status-box {
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
        }
        .success-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .info-box {
            background-color: #d1ecf1;
            border: 1px solid #b8daff;
            color: #0c5460;
        }
    </style>
    """, unsafe_allow_html=True)