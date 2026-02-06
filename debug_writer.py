from agents.writer_agent import writer_agent
from state import AgentState
from dotenv import load_dotenv
import os

load_dotenv()

def debug_writer():
    print("DEBUG: Starting Writer Agent Test")
    
    # Mock efficient state from Planner
    mock_state = {
        "topic": "Test Topic",
        "slide_count": 2,
        "font": "Arial",
        "depth": "Concise",
        "presentation_outline": [
            {"title": "Introduction", "description": "Intro to the topic"},
            {"title": "Key Points", "description": "Main concepts"}
        ],
        "slide_content": [], # Empty initially
        "final_ppt_path": ""
    }
    
    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY not found in env")
        return

    try:
        result = writer_agent(mock_state)
        print("\nDEBUG: Writer Agent Result:")
        print(result)
        
        slides = result.get("slide_content", [])
        print(f"\nDEBUG: Generated {len(slides)} slides.")
        for i, slide in enumerate(slides):
            print(f"Slide {i+1} Title: {slide.get('title')}")
            content = slide.get('content', '')
            print(f"Slide {i+1} Content Length: {len(content)}")
            print(f"Slide {i+1} Content Sample: {content[:50]}...")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug_writer()
