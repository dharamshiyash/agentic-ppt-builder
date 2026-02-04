from agentic_ppt_builder.state import AgentState
from agentic_ppt_builder.utils.ppt_utils import create_presentation
import os

def ppt_builder_agent(state: AgentState):
    print("--- PPT BUILDER AGENT ---")
    slides = state['slide_content']
    font = state['font']
    
    # Define output path
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{state['topic'].replace(' ', '_')}_presentation.pptx"
    output_path = os.path.join(output_dir, filename)
    
    final_path = create_presentation(slides, font_name=font, output_path=output_path)
    
    print(f"Presentation saved to: {final_path}")
    
    return {"final_ppt_path": final_path}
