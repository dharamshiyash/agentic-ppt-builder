from agentic_ppt_builder.graph import build_graph
import os
from dotenv import load_dotenv

load_dotenv()

def run_verification():
    print("Starting verification...")
    
    if not os.getenv("GROQ_API_KEY"):
        print("SKIP: No GROQ_API_KEY found in env.")
        return

    app = build_graph()
    
    initial_state = {
        "topic": "Artificial Intelligence in 2025",
        "slide_count": 3,
        "font": "Arial",
        "depth": "Concise",
        "presentation_outline": [],
        "slide_content": [],
        "final_ppt_path": ""
    }
    
    print("Invoking graph...")
    try:
        final_state = app.invoke(initial_state)
        
        ppt_path = final_state.get("final_ppt_path")
        if ppt_path and os.path.exists(ppt_path):
            print(f"SUCCESS: PPT generated at {ppt_path}")
        else:
            print("FAILURE: PPT path missing or file not found.")
            
    except Exception as e:
        print(f"FAILURE: Exception during graph execution: {e}")

if __name__ == "__main__":
    run_verification()
