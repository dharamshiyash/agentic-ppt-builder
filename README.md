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
-   **LLM**: ChatGroq (Llama-3 70B)`
-   **Presentation**: `python-pptx`

## 🚀 How to Run

1.  **Clone the repository** (if applicable).
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up Environment**:
    -   Create a `.env` file (optional) or enter keys in the UI.
    -   Required keys: `GROQ_API_KEY`.
    -   Optional: `UNSPLASH_ACCESS_KEY` (for real images).

4.  **Run the App**:
    ```bash
    streamlit run agentic_ppt_builder/app.py
    ```

## 📂 Project Structure

```
agentic_ppt_builder/
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
