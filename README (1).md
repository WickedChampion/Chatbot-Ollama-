# 🧠 Local LLM Chatbot with History --- Powered by Ollama & Streamlit

A lightweight, privacy-focused AI chatbot that runs **completely
locally** using **Ollama**.\
This project includes:

-   🚀 Local inference using the Ollama LLM\
-   💬 Chat history (persistent storage in JSON)\
-   🌐 Streamlit UI for clean and fast interactions\
-   ⚡ Modular backend architecture with APIs\
-   🔧 Easy to customize, extend, and run locally

Perfect for beginners learning **Ollama**, **local LLM workflows**,
**Streamlit**, and **API design**.

------------------------------------------------------------------------

## ✨ Features

### 🔹 1. Local LLM Powered by Ollama

The chatbot uses an Ollama model (defaults to `llama3`) and works
**fully offline**.

### 🔹 2. Chat History (Persistent)

The entire conversation is stored in:

    history.json

### 🔹 3. Streamlit UI

A smooth, clean interface to chat with the model.

### 🔹 4. FastAPI Backend (Optional)

Backend API that handles: - Generating responses - Storing messages -
Retrieving chat history

### 🔹 5. Easy Setup

Just run:

    uvicorn main:app
    streamlit run ui.py

------------------------------------------------------------------------

## 📂 Project Structure

    📦 ollama-chatbot
     ┣ 📜 main.py
     ┣ 📜 chat_history.json
     ┣ 📜 ui.py
     ┣ 📜 requirements.txt
     ┗ 📜 README.md

------------------------------------------------------------------------

## 🛠️ Installation

### 1️⃣ Install Ollama

https://ollama.com/download

    ollama pull llama3

### 2️⃣ Clone repository

    git clone https://github.com/yourusername/ollama-chatbot.git
    cd ollama-chatbot

### 3️⃣ Install dependencies

    pip install -r requirements.txt

------------------------------------------------------------------------

## ▶️ Running

Start backend:

    uvicorn main:app --reload

Start UI:

    streamlit run ui.py

------------------------------------------------------------------------

## 📡 API Endpoints

  Method   Endpoint      Description
  -------- ------------- ----------------
  POST     `/generate`   Generate reply
  GET      `/history`    Fetch history

------------------------------------------------------------------------

## 🚀 Future Enhancements

-   RAG\
-   PDF/Text upload\
-   Multi-model switching\
-   Voice support

------------------------------------------------------------------------

## 🤝 Contributing

PRs welcome.

------------------------------------------------------------------------

## 📜 License

MIT License.
