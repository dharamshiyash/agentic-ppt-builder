# 🤖 Agentic AI PowerPoint Builder

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-blueviolet)](https://langchain-ai.github.io/langgraph/)

A production-ready, multi-agent AI system that autonomously researches, plans, writes, and builds professional PowerPoint presentations. Powered by **LangGraph**, **Groq (Llama 3)**, and **Streamlit**.

---

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for planning, writing, image sourcing, and slide building.
- **Agentic Workflow**: Linear graph orchestration using LangGraph for robust state management.
- **Smart Image Integration**: Automatically fetches relevant, royalty-free stock images via Unsplash.
- **Production Grade**:
  - **Modular Design**: Clean separation of concerns (Service/Agent/Schema pattern).
  - **Caching Layer**: Persisted disk cache for LLM & API calls to reduce costs and latency.
  - **Structured Logging**: Comprehensive logging for observability.
  - **Configuration Management**: Centralized environment handling.
- **Interactive UI**: User-friendly Streamlit interface for easy generation.

---

## 🏗 Architecture

The system operates as a pipeline of specialized agents:

1.  **Planner Agent** (`agents/planner`):
    *   **Role**: Architect.
    *   **Input**: Topic, Slide Count.
    *   **Output**: Structured JSON outline of slide titles and descriptions.
    *   *Does not generate full content.*

2.  **Writer Agent** (`agents/writer`):
    *   **Role**: Content Creator.
    *   **Input**: Slide Outline.
    *   **Output**: Detailed bullet points and narrative text for each slide.

3.  **Image Agent** (`agents/image`):
    *   **Role**: Visual Designer.
    *   **Input**: Slide Content.
    *   **Output**: Selection of relevant stock image URLs.
    *   *Uses intelligent keyword extraction.*

4.  **Builder Agent** (`agents/builder`):
    *   **Role**: Publisher.
    *   **Input**: Final structured data.
    *   **Output**: `.pptx` file with professional layout.

---

## 🛠 Installation

### Prerequisites

- Python 3.10 or higher
- [Groq API Key](https://console.groq.com/) (for LLM)
- [Unsplash Access Key](https://unsplash.com/developers) (for Images)

### Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/dharamshiyash/agentic-ppt-builder.git
    cd agentic-ppt-builder
    ```

2.  **Create Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment**
    Copy the example environment file and add your API keys:
    ```bash
    cp .env.example .env
    ```
    Open `.env` and fill in your keys:
    ```ini
    GROQ_API_KEY=gsk_...
    UNSPLASH_ACCESS_KEY=...
    ```

---

## ▶️ Usage

### Run the App
Launch the Streamlit interface:
```bash
streamlit run app.py
```

### Generated Outputs
Presentations are saved in the `outputs/` directory by default.

---

## 🧪 Testing

Run the automated test suite to verify system integrity:

```bash
pytest
```

---

## 📂 Project Structure

```
.
├── agents/             # Agent modules (Planner, Writer, Image, Builder)
│   ├── planner/        # Planner Agent logic
│   ├── writer/         # Writer Agent logic
│   ├── image/          # Image Agent logic
│   └── builder/        # PPT Builder Agent logic
├── tools/              # Shared tools (Caching, etc.)
├── utils/              # Utilities (Config, Logger)
├── tests/              # Unit and Integration tests
├── app.py              # Streamlit Entrypoint
├── graph.py            # LangGraph Orchestration
├── requirements.txt    # Dependencies
└── README.md           # Documentation
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

**Author**: Yash Dharamshi
