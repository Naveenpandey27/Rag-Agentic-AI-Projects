# LawAI

A Retrieval‑Augmented Generation (RAG) and Agentic AI project geared toward legal applications.

## 📘 Introduction

LawAI uses modern LLMs with RAG techniques to ingest legal documents, build a vector store, and facilitate efficient case‑law retrieval and question answering.

<img width="1910" height="621" alt="ll" src="https://github.com/user-attachments/assets/8b176b1d-393a-4494-b6cf-2134ed72dd8b" />

**Demo link**
https://rag-agentic-ai-projects-fjcpbp5dc9emfu8hlm9q3f.streamlit.app/
## 🔧 Features

* **Document loader**: Parses legal case files (e.g., PDF, plain text).
* **Chunking strategy**: Splits documents into overlapping chunks for improved search.
* **Embedding & vector store**: Uses embedding models (e.g., HuggingFace) with FAISS.
* **Retrieval & QA pipeline**: Supports QA chains over retrieved legal context.
* **Agentic flow**: Optionally supports multi‑agent architecture—combining retrieval, web search, and filtering agents.

## ⚙️ Installation

```bash
git clone https://github.com/Naveenpandey27/Rag-Agentic-AI-Projects.git
cd Rag-Agentic-AI-Projects/LawAI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Adjust chunk size, overlap, retrieval depth, or model endpoints as needed.

## ⚙️ Configuration

* **Chunk settings**: `chunk_size`, `chunk_overlap`
* **Embedding model**: e.g. `all-MiniLM-L6-v2`
* **Vector store**: FAISS (or replaceable with Chroma, Pinecone, etc.)
* **LLM endpoint**: OpenAI, HuggingFace, Ollama—configurable via env vars or presets.

## 🛠 Troubleshooting

* If missing results: increase retrieval depth or reduce chunk size.
* Ensure legal PDF files aren’t corrupted.
* Vector store fails? Rebuild embeddings from scratch.
* LLM responds slowly/unavail? Verify API keys and endpoints.

## 👥 Contributors

* **Naveen Pandey** – repository author and maintainer.
