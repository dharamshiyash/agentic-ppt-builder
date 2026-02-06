from graph import build_graph
import os
from dotenv import load_dotenv

load_dotenv()

def debug_full_pipeline():
    print("DEBUG: Starting Full Pipeline Trace")
    
    app = build_graph()
    
    initial_state = {
        "topic": "Future of AI",
        "slide_count": 2,
        "font": "Arial",
        "depth": "Concise",
        "presentation_outline": [],
        "slide_content": [],
        "final_ppt_path": ""
    }
    
    print("\nDEBUG: Invoking Graph...")
    try:
        # Stream the graph to see updates step-by-step
        for output in app.stream(initial_state):
            for key, value in output.items():
                print(f"\n--- Node '{key}' Finished ---")
                if key == "planner":
                    outline = value.get("presentation_outline", [])
                    print(f"DEBUG: Planner produced {len(outline)} items.")
                    print(f"DEBUG: Sample: {outline[0] if outline else 'None'}")
                elif key == "writer":
                    slides = value.get("slide_content", [])
                    print(f"DEBUG: Writer produced {len(slides)} slides.")
                    if slides:
                        print(f"DEBUG: Sample Slide 1 Title: {slides[0].get('title')}")
                        print(f"DEBUG: Sample Slide 1 Content Length: {len(slides[0].get('content', ''))}")
                elif key == "image_agent":
                     slides = value.get("slide_content", [])
                     print(f"DEBUG: Image Agent processed {len(slides)} slides.")
                     if slides:
                        print(f"DEBUG: Sample Slide 1 Image URL: {slides[0].get('image_url')}")
                elif key == "ppt_builder":
                    print(f"DEBUG: PPT Path: {value.get('final_ppt_path')}")
                    
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    debug_full_pipeline()
