import os

os.environ["OTEL_PYTHON_DISABLED"] = "true"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = ""

from dotenv import load_dotenv
import streamlit as st
from langchain.chat_models import ChatOllama
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import re

# Load environment variables (optional)
load_dotenv()

# Constants
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DB_DIR = "db"
OLLAMA_MODEL = "deepseek-r1"  # Use DeepSeek 1.5 via Ollama
LLM_TEMPERATURE = 0.2  # Adjust temperature for response determinism

# 1. Initialize the Ollama-powered LLM via LangChain
llm = ChatOllama(model=OLLAMA_MODEL, temperature=LLM_TEMPERATURE)

# 2. Load vector database and retriever
embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)
vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_kwargs={"k": 4})

# 3. Define a system prompt template
template = """
You are Lorenzo Cárdenas, a data scientist and ML engineer. Use the provided context to answer the user concisely and accurately in first person.

Do not include any internal reasoning or thought process. Provide only the final, polished answer.

Context:
{context}

Question: {question}
Answer:
"""
prompt = PromptTemplate(input_variables=["context", "question"], template=template)

# 4. Build RetrievalQA chain with custom prompt
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},
    return_source_documents=False
)

# 5. Streamlit UI

def clean_answer(answer: str) -> str:
    # Remove any <think>...</think> sections
    return re.sub(r"<think>[\s\S]*?<\/think>", "", answer, flags=re.IGNORECASE).strip()


def send_query():
    user_query = st.session_state.user_input
    if user_query:
        with st.spinner("Thinking..."):
            raw_answer = qa_chain.run(user_query)
        answer = clean_answer(raw_answer)
        st.session_state.history.append((user_query, answer))
        st.session_state.user_input = ""

st.set_page_config(page_title="Ask Lorenzo - Chatbot", layout="wide")
st.title("🤖 Ask Lorenzo Cárdenas: Professional Background Chatbot")

if "history" not in st.session_state:
    st.session_state.history = []

# Text input with Enter key binding
st.text_input(
    "Ask me about my background, skills, or projects:",
    key="user_input",
    on_change=send_query
)

# Display chat history
for q, a in reversed(st.session_state.history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Bot:** {a}")
    st.markdown("---")
