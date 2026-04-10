# Multimodal Medical Report Analyzer 🏥

A specialized AI assistant designed for medical professionals and patients. It analyzes medical reports, documents (PDFs), and images  using advanced LLMs (Llama 4 Scout) to provide health-related insights.

## ✨ Features

-   **Strict Medical Domain**: The AI is restricted to medical topics only. It validates all uploaded content and text queries, rejecting non-medical inputs (e.g., recipes, general coding).
-   **Multimodal Analysis**: 
    -   **PDF Reports**: Extract and analyze text from medical PDF documents.
    -   **Medical Imaging**: Analyze medical images for insights.
-   **Persistent History**: All chat sessions are securely stored in a local SQLite database (`chat.db`).
-   **Modern UI**:
    -   Streamlined sidebar with one-click access to previous sessions.
    -   Clean, distraction-free chat interface.
    -   Dark mode optimization.

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   [Groq API Key](https://console.groq.com/keys)

### Installation



1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment**:
    Create a `.env` file:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

### Usage

Run the application:
```bash
streamlit run app.py
```
*Or use the helper script:*
```bash
./run.sh
```

## 📂 Project Structure

```
multimodal-analyzer/
├── app.py              # Main application logic
├── database.py         # SQLite database management
├── assets/             # UI assets (CSS, HTML)
├── chat.db             # Local database (created on run)
├── requirements.txt    # Dependencies
├── .env                # Configuration
└── run.sh              # Launcher script
```

## 🛠️ Built With

-   **Streamlit** - Frontend Framework
-   **Groq API** - Llama 4 Scout (Multimodal LLM)
-   **SQLite** - Data Persistence
-   **PyPDF2** & **Pillow** - File Processing

---
