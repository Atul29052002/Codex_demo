# AI Report Narration Studio (Streamlit + LangChain)

This project is a simple web-based narration generator for analytics reports.

## What it uses

- **Streamlit** for UI
- **LangChain** orchestration
- **Chroma DB** and **FAISS** vector retrieval options
- **Ollama LLM** (`llama3.2` by default) for narrative generation
- **Ollama embeddings** (`nomic-embed-text` by default)

## Quick start

```bash
pip install -r requirements.txt
# Ensure Ollama is running locally and models are available:
# ollama pull llama3.2
# ollama pull nomic-embed-text
streamlit run app.py
```

## How it works

1. Generates synthetic monthly KPI data by region/product.
2. Converts KPI slices into LangChain `Document` objects.
3. Indexes documents in either **Chroma** or **FAISS**.
4. Retrieves evidence for a user narration query.
5. Uses Ollama LLM to generate concise executive narration.

## Notes

- If generation fails, verify local Ollama daemon/model availability.
- You can switch vector backend in the sidebar to compare retrieval behavior.
