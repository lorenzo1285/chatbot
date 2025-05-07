# Code/build_db.py

import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# 1) Load environment (if you ever switch to OpenAI embeddings)
load_dotenv()

# 2) Load your profile document
loader = TextLoader("Data/profile.md")
docs = loader.load()

# 3) Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 4) Create embeddings
emb_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 5) Build & persist your Chroma DB
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=emb_model,
    persist_directory="db"
)
vectordb.persist()

print("✅ Vector database built and saved to ./db")
