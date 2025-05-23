# -*- coding: utf-8 -*-
"""RAG Implementation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1biWq9MZa712xwwUKrQtySEUY_Vf4YPvg

[**Install All Dependencies**](https://)
"""

!pip install langchain-community pymupdf sentence-transformers faiss-cpu

!pip install --upgrade langchain

!pip install pymupdf

!pip install --upgrade langchain_community pymupdf faiss-cpu

!pip install langchain transformers sentence-transformers faiss-cpu pypdf

"""**This notebook implements a PDF Question Answering system using Retrieval-Augmented Generation (RAG). It loads a PDF document, splits the content into manageable chunks, and uses FAISS for efficient document retrieval based on semantic similarity. The system then leverages a HuggingFace-based LLM (Gemma-7B) for generating context-aware answers. The process ensures that responses are fact-based and reliable by grounding them in the document's actual content, overcoming common limitations of LLMs like hallucinations and overgeneralization.**"""

!pip install -q langchain langchain-community langchain-core faiss-cpu pymupdf sentence-transformers
!pip install -q transformers accelerate bitsandbytes

from google.colab import files
uploaded = files.upload()

from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline
import torch

pdf_path = "/content/drive/MyDrive/Rosalind Franklin_ The Dark Lady of DNA.pdf" # Takes the first uploaded PDF
loader = PyMuPDFLoader(pdf_path)
docs = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
documents = text_splitter.split_documents(docs)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(documents, embedding_model)

model_id = "unsloth/gemma-7b-it"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype=torch.float16)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=512)
llm = HuggingFacePipeline(pipeline=pipe)


retriever = db.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)


query = "Summarize the document."
result = qa_chain.run(query)
print("Answer:", result)

#Test the model with a specific question
query = "Who is Rosalind Franklin and what was her contribution to DNA research?"
result = qa_chain.run(query)
print("Answer:", result)

#Test another specific question
query_2 = "Explain the significance of Rosalind Franklin's X-ray images in the discovery of DNA's structure."
result_2 = qa_chain.run(query_2)
print("Answer:", result_2)

query = "Who contributed to the discovery of the DNA double helix?"
result = qa_chain.run(query)
print("Answer:", result)

"""**Correct Specific answer**"""

query = "Rosalind Franklin’ life after death?"
result = qa_chain.run(query)
print("Answer:", result)

"""**The model only generates responses when it has enough relevant information, avoiding speculation or the provision of uncertain answers.**"""

query = "Rosalind Franklin’s love life"
result = qa_chain.run(query)
print("Answer:", result)