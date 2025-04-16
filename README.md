# RAG-Implementation
Architectural Overview:
This model uses Retrieval-Augmented Generation (RAG) to improve PDF Question Answering by combining semantic search with contextual generation. The document is loaded and split using PyMuPDF and CharacterTextSplitter, then embedded with Sentence-Transformers and stored in FAISS for fast retrieval. Gemma-7B LLM generates answers based on the retrieved context, ensuring accurate and fact-based responses.
