## 🧠 BrieflyAI

A Retrieval-Augmented Generation (RAG) and Agentic AI demo built with modern LLM frameworks & MCP, designed to fetch context from web and generate concise summaries.


## Demo

<img width="1842" height="767" alt="brrr" src="https://github.com/user-attachments/assets/7340e96f-5c4e-4a27-8171-9ac0ca0ec4d7" />

---

## 🚀 Table of Contents
- [Introduction](#introduction)  
- [Features](#features)  
- [Architecture](#architecture)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Usage](#usage)  
- [Project Structure](#project-structure)  
- [Contributing](#contributing)  
---

## 🎯 Introduction


![Uploading brrr.png…]()

**BrieflyAI** is a lightweight RAG-powered AI tool that retrieves relevant information from a knowledge base or live web searches and generates concise summaries using an agentic decision-making flow :contentReference[oaicite:1]{index=1}.



---

## ✨ Features
- **Context-aware Summarization**: Retrieves relevant documents or web snippets then summarizes them briefly.
- **Agentic Workflow**: Dynamically decides between static knowledge retrieval and live web search.
- **Modular Design**: Easily plug in different LLMs, vector DBs, or search APIs.
- **Flexible Deployment**: Runs locally or via API, with CLI or GUI support for interaction.

---

## 🏗️ Architecture

1. **Query Input**: User submits a request.
2. **Router Agent**: Chooses between retrieving from local docs or performing web search.
3. **Retrieval**:
   - **Vector DB**: Embed and fetch local documents.
   - **Web Search**: Use API (e.g. Bing/Tavily) if local context is insufficient.
4. **Summarization**: LLM generates a concise summary from retrieved content.
5. **Evaluation & Reasoning**: Agent checks summary, detects hallucinations, and refines output.

---

## 🎬 Getting Started

### Prerequisites
- Python 3.10+  
- Pip or Conda package manager  
- [Optional] API keys:
  - Vector DB (Chroma, FAISS, etc.)
  - Web search (e.g. Tavily, Bing)

### Installation

```bash
# Clone the repository
git clone https://github.com/Naveenpandey27/Rag-Agentic-AI-Projects.git
cd Rag-Agentic-AI-Projects/BrieflyAI/

# Setup environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
````

### Usage

```bash
# Interactive CLI
python run_briefly.py --query "Explain quantum entanglement"

# API server
uvicorn app:app --reload
curl http://localhost:8000/summarize -X POST -d '{"query":"..."}'
```

Modify `config.yaml` to switch LLMs, vector DBs, or search services.

---

## 📁 Project Structure

```
BrieflyAI/
├── app/                  # API server code
├── docs/                 # Documents for vector DB ingestion
├── agents/               # Agent logic (router, evaluator)
├── embeddings.py         # Vector embedding utilities
├── retriever.py          # Retrieval pipeline
├── summarizer.py         # LLM summarization interface
├── run_briefly.py        # CLI tool entry point
├── requirements.txt
└── config.yaml           # Configuration file (API keys, model settings)
```
`

Set API keys via env vars:

```bash
export GROQ_API_KEY=...
export BRIGHTDATA_API_KEY = ...
```


## 🙌 Acknowledgements

* Idea & base structure from RAG/Agentic AI collection by **Naveenpandey27**
