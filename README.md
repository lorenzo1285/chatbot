# Ask Lorenzo: Professional Background Chatbot

A local, self‑hosted chatbot that answers questions about Lorenzo Cárdenas’s professional background, powered by:

* **LangChain** for retrieval and conversational logic
* **Chroma** vector database with `sentence-transformers` embeddings
* **Ollama** serving the DeepSeek‑R1 (1.5B)
* **Streamlit** for a lightweight, interactive web UI

---

## 🚀 Features

* **Retrieval‑Augmented Generation (RAG):** Queries your markdown profile (`Data/profile.md`) for context.
* **Vector Search:** Chunks and embeds your profile into a Chroma DB for fast semantic lookup.
* **On‑Premise LLM:** Runs models locally via Ollama—no external API calls.
* **Interactive UI:** Press **Enter** to send a question; view an ongoing chat history.
* **Configurable:** Easily switch models or adjust `temperature`.

---

## 📦 Getting Started

### Prerequisites

* **Python 3.10+**
* **Git**
* **Ollama CLI** installed and configured
* **Virtual environment** (recommended)

### Clone the Repo

```bash
git clone https://github.com/lorenzo1285/chatbot.git
cd chatbot
```

### Create & Activate a Virtual Environment

```bash
python -m venv env_chatbot
# Windows (CMD):
env_chatbot\Scripts\activate
# macOS/Linux:
source env_chatbot/bin/activate
```

### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Set Up Secrets

Create a file at `.streamlit/secrets.toml` with any tokens you need (e.g., Hugging Face), for example:

```toml
# .streamlit/secrets.toml
OLLAMA_API_KEY = "your_ollama_token_here"
```

> **Note:** Make sure `.env` files and the `db/` directory are listed in `.gitignore`.

---

## ⚙️ Building the Vector Database

Whenever you update `Data/profile.md`, rebuild the Chroma store:

```bash
# Remove old DB
rm -rf db  # macOS/Linux
# or (Windows CMD)
rmdir /S /Q db

# (Re)build embeddings
python Code/build_db.py
```

This creates a fresh `db/` directory with semantic embeddings of your profile.

---

## ▶️ Running Locally

Ensure Ollama is running your chosen model, e.g.:

```bash
ollama pull deepseek-r1
ollama run deepseek-r1
```

Then start your Streamlit app:

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Open your browser at `http://localhost:8501` to begin chatting.

---

## 🌐 Streamlit Cloud Deployment

1. **Make the repo public** (or link a paid account).
2. Ensure `app.py` and `requirements.txt` are at the repo root.
3. Push to GitHub on `main`.
4. In Streamlit Cloud, set:

   * **Repository:** `lorenzo1285/chatbot`
   * **Branch:** `main`
   * **Main file path:** `app.py`
5. Click **Deploy**. Your chatbot will be live at `https://<your-username>-chatbot.streamlit.app/`.

---

## 🔧 Configuration

* **Change LLM model:** edit the `OLLAMA_MODEL` constant in `app.py` or use the sidebar selector if enabled.
* **Temperature:** adjust `LLM_TEMPERATURE` for more creative (`>0.5`) or deterministic (`<0.2`) responses.
* **Retrieval size:** tune `k` in `vectordb.as_retriever(search_kwargs={"k": 4})`.

---

## 🛠️ Folder Structure

```
chatbot/
├── app.py               # Streamlit entry point
├── Code/
│   ├── build_db.py      # Embedding & DB builder
│   └── inspect_db.py    # DB inspection utility
├── Data/
│   └── profile.md       # Your professional profile
├── db/                  # Generated Chroma vector store
├── requirements.txt     # Python dependencies
└── .streamlit/
    └── secrets.toml     # API tokens (ignored by Git)
```

---

## 🙋‍♂️ Troubleshooting

* **`st.session_state` errors:** ensure you’re not reassigning widget keys mid-run—use callbacks instead.
* **Docker compose issues:** refer to the provided `docker-compose.yml` sample in docs for production deploy.
* **Model loading errors:** confirm Ollama models are pulled and running (`ollama list`).

---

## 🔗 Useful Links

* [LangChain Docs](https://langchain.com)
* [Ollama Docs](https://ollama.com/docs)
* [Chroma DB](https://chromadb.com)
* [Streamlit Deploy Guide](https://docs.streamlit.io/streamlit-cloud)

---

*Created by Lorenzo Cárdenas — Data Scientist & AI Engineer*
