# 🏥 Multimodal Medical Report Analyzer

A specialized AI assistant designed for medical professionals and patients. It analyzes medical reports, PDFs, and medical images using advanced multimodal LLMs to generate meaningful health insights.

---

## ✨ Features

* **Strict Medical Domain**

  * Accepts only medical-related queries and files
  * Rejects irrelevant inputs (e.g., coding, recipes)

* **Multimodal Analysis**

  * 📄 Extracts and analyzes **medical PDFs**
  * 🖼️ Interprets **medical images**

* **Persistent Chat History**

  * Stores all sessions securely using local database (`chat.db`)

* **Modern UI**

  * Clean chat interface
  * Sidebar with session history
  * Dark mode optimized

---

## 🧠 Architecture Overview

### 🔄 Workflow

1. **User Input**

   * Text / PDF / Image

2. **Validation Layer**

   * Filters strictly medical content

3. **Processing Layer**

   * PDF → Text extraction
   * Image → Vision processing

4. **LLM Orchestration**

   * Managed via **LangChain**
   * Stateful flow using **LangGraph**

5. **Inference**

   * Powered by Llama 4 Scout via Groq API

6. **Storage**

   * SQLite database

7. **Frontend**

   * Streamlit UI

## ⚙️ Tech Stack

* Streamlit – Frontend framework
* Groq API – Fast LLM inference
* Llama 4 Scout – Multimodal AI model
* LangChain – LLM orchestration
* LangGraph – Stateful workflows
* SQLite – Local database
* PyPDF2 – PDF text extraction
* Pillow – Image processing

---

## 🚀 Getting Started

### 📌 Prerequisites

* Python 3.10+
* Groq API Key

---

### 🔧 Installation

```bash
pip install -r requirements.txt
```

---

### 🔐 Environment Setup

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

### ▶️ Run the App

```bash
streamlit run app.py
```

**OR**

```bash
./run.sh
```

---

## 📂 Project Structure

```
multimodal-analyzer/
├── app.py              # Main app
├── database.py         # DB handling
├── assets/             # UI assets
├── chat.db             # SQLite DB
├── requirements.txt    # Dependencies
├── .env                # Config
└── run.sh              # Script
```

---

## 🚀 Future Improvements

* 🔍 RAG with medical knowledge base
* 🧬 Clinical ontology integration
* 📊 Report dashboards
* 🔐 HIPAA-compliant deployment
* 🧠 Fine-tuned medical models

---

## ⚠️ Disclaimer

This tool is for **informational purposes only** and does not replace professional medical advice, diagnosis, or treatment.

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repo and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---
