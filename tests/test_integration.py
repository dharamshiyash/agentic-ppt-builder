
import pytest
from unittest.mock import patch, MagicMock
from agentic_ppt_builder.graph import build_graph

def test_full_pipeline_mocked():
    """Run the Full Graph with mocked agents to ensure flow is correct."""
    
    initial_state = {
        "topic": "Integration Test",
        "slide_count": 2,
        "font": "Arial",
        "depth": "Concise",
        "presentation_outline": [],
        "slide_content": [],
        "final_ppt_path": ""
    }
    
    # We patch the AGENT functions themselves to strictly control output and avoid API calls
    with patch('agentic_ppt_builder.graph.planner_agent') as mock_planner, \
         patch('agentic_ppt_builder.graph.writer_agent') as mock_writer, \
         patch('agentic_ppt_builder.graph.image_agent') as mock_image, \
         patch('agentic_ppt_builder.graph.ppt_builder_agent') as mock_builder:
         
        # Setup returns
        mock_planner.return_value = {"presentation_outline": [{"title": "T1", "description": "D1"}]}
        mock_writer.return_value = {"slide_content": [{"title": "T1", "content": "C1", "image_keyword": None, "image_url": None}]}
        mock_image.return_value = {"slide_content": [{"title": "T1", "content": "C1", "image_keyword": "K1", "image_url": "U1"}]}
        mock_builder.return_value = {"final_ppt_path": "output.pptx"}
        
        # Build graph INSIDE the patch context so it picks up the mocks
        app = build_graph()
        
        # Run graph
        result = app.invoke(initial_state)
        
        # Verify result contains the final path
        assert result['final_ppt_path'] == "output.pptx"
        
        # Verify flow
        mock_planner.assert_called()
        mock_writer.assert_called()
        mock_image.assert_called()
        mock_builder.assert_called()
