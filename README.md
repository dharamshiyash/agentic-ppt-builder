# Agentic AI PowerPoint Builder 🚀

A multi-agent AI system that generates professional PowerPoint presentations based on user inputs.
Powered by **LangGraph**, **Groq**, and **Unsplash**.

## 🏗 Architecture

The system uses 4 collaborative agents orchestrated via LangGraph:

1.  **Slide Planner Agent**: Structures the presentation outline.
2.  **Content Writer Agent**: Writes detailed content for each slide.
3.  **Visual & Image Agent**: Selects relevant images for slides.
4.  **PPT Builder Agent**: Compiles everything into a `.pptx` file.

## 🛠 Tech Stack

-   **Frontend**: Streamlit
-   **Backend**: Python, LangGraph
-   **LLM**: ChatGroq (Llama-3 70B)
-   **Presentation**: `python-pptx`

## 🛠️ Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/dharamshiyash/agentic-ppt-builder.git
    cd agentic-ppt-builder
    ```

2.  **Create Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Mac/Linux
    # venv\Scripts\activate  # Windows
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration**
    Copy the example env file and add your API keys:
    ```bash
    cp .env.example .env
    ```
    Edit `.env`:
    ```env
    GROQ_API_KEY=your_key_here
    UNSPLASH_ACCESS_KEY=your_key_here
    ```

## 🚀 Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

## 🧪 Testing

This project includes a comprehensive test suite using `pytest`.

To run all tests:
```bash
pytest -v
```

See [docs/testing_report.md](docs/testing_report.md) for detailed test cases.

## 📦 Deployment (Streamlit Cloud)

1.  Push code to GitHub.
2.  Log in to [Streamlit Cloud](https://streamlit.io/cloud).
3.  Create a new app and select this repository.
4.  In "Advanced Settings", add your secrets (`GROQ_API_KEY`, `UNSPLASH_ACCESS_KEY`).
5.  Click **Deploy**.

## 📂 Project Structure
│── app.py                  # Streamlit Frontend
│── agents/                 # AI Agents
│── utils/                  # Helper functions
│── graph.py                # LangGraph Orchestration
│── state.py                # Shared State
│── outputs/                # Generated PPTs
```

## ✨ Features

-   Customizable Slide Count & Depth.
-   Choice of Fonts.
-   Automatic Image Fetching.
-   Professional `.pptx` Export.
