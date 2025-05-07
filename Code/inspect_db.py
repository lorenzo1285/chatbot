# inspect_db.py

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

# 1) Initialize the same embeddings you used to build the DB
emb_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2) Load your persisted vectorstore
vectordb = Chroma(persist_directory="db", embedding_function=emb_model)

# 3) Pull all stored chunks and metadata
collection = vectordb._collection
data = collection.get(include=["documents", "metadatas"])

# 4) Print them out
for i, (doc, meta) in enumerate(zip(data["documents"], data["metadatas"])):
    print(f"--- Chunk #{i+1} ---")
    print(doc)
    if meta:
        print("Metadata:", meta)
    print()
