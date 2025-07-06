# Rag-Agentic-AI-Projects
A collection of RAG (Retrieval-Augmented Generation) and Agentic AI projects showcasing intelligent retrieval, reasoning, and decision-making workflows using modern LLM frameworks.



# History Assistant - AI-Powered Historical Exploration Tool

![history_assistant](https://github.com/user-attachments/assets/b8b1beb8-21bb-4e6d-a90d-0f9310925d98)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [API Requirements](#api-requirements)
- [Contributing](#contributing)

## Overview

The History Assistant is an AI-powered application that helps users explore and understand historical events, figures, and civilizations. Powered by Groq's lightning-fast LLM inference and LangChain, this tool provides engaging, accurate historical information with scholarly precision.

Key capabilities:
- Interactive Q&A about any historical topic
- Comprehensive coverage from ancient to modern history
- Contextual understanding of historical events
- Multi-perspective analysis of controversial topics
- Engaging storytelling approach

## Features

✨ **AI-Powered Insights**
- Powered by Groq's ultra-fast LLM inference
- Uses Llama-3.3-70b model for accurate historical information
- Real-time responses with scholarly depth

🌍 **Comprehensive Historical Coverage**
- Ancient civilizations (Egypt, Greece, Rome)
- Medieval and Renaissance periods
- Modern history (Industrial Revolution, World Wars)
- Contemporary historical events
- Global historical perspectives

💡 **Interactive Learning Experience**
- Suggested topic prompts
- Contextual follow-up questions
- Visual timeline integration (future)
- Source citations (future)

🎨 **Beautiful Interface**
- Responsive design
- Themed chat interface
- Mobile-friendly layout
- Accessible color scheme

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Groq API key (free tier available)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/history-assistant.git
cd history-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your Groq API key:
```env
GROQ_API_KEY=your_api_key_here
```

## Usage

### Running the Application
```bash
streamlit run main.py
```

The application will launch in your default browser at `http://localhost:8501`

### Basic Workflow
1. Enter your Groq API key in the sidebar
2. Choose from suggested topics or type your own question
3. View the AI-generated historical analysis
4. Ask follow-up questions for deeper exploration

### Example Questions
- "Explain the causes of the French Revolution"
- "Compare Greek and Roman political systems"
- "What were the key outcomes of the Yalta Conference?"
- "Describe daily life in medieval Europe"

## Configuration

The application can be configured through several methods:

### Environment Variables
- `GROQ_API_KEY`: Your Groq API key (required)
- `MODEL_NAME`: Override default model (default: "llama-3.3-70b-versatile")
- `MAX_TOKENS`: Response length limit (default: 4000)

### UI Settings
Available in the sidebar:
- API key input
- Suggested topics
- Chat clearing option

### Code Configuration
Modify `utils/config.py` for:
- Page layout settings
- Default messages
- Model parameters

## Project Structure

```
history_assistant/
├── main.py                # Main application entry point
├── utils/                 # Utility functions and configurations
│   ├── __init__.py
│   ├── config.py          # App configuration and constants
│   ├── helpers.py         # Helper functions
│   ├── styles.py          # CSS and UI styling
├── services/              # Business logic services
│   ├── __init__.py
│   ├── groq_service.py    # Groq API interactions
│   ├── chat_service.py    # Chat message handling
├── templates/             # Prompt templates
│   ├── __init__.py
│   ├── prompts.py         # LLM prompt templates
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variables template
```

## API Requirements

This application requires a Groq API key. You can obtain one for free:

1. Sign up at [Groq Cloud](https://console.groq.com)
2. Navigate to API Keys
3. Create a new key
4. Copy the key and add it to your `.env` file

The free tier provides sufficient access for personal and testing use.

## Contributing

I welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

### Areas for Contribution
- Additional historical topic coverage
- UI/UX improvements
- Testing and quality assurance
- Documentation enhancements
- Localization support

## Acknowledgments

- Groq for their powerful inference API
- LangChain team for the excellent framework
- Streamlit for the intuitive app framework
- All historical scholars whose work informs this tool
