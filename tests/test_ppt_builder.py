
import pytest
import os
from unittest.mock import patch, MagicMock
from agents.ppt_builder_agent import ppt_builder_agent

def test_ppt_builder_no_slides(mock_agent_state):
    result = ppt_builder_agent(mock_agent_state)
    assert result['final_ppt_path'] == ""

def test_ppt_builder_success(mock_agent_state, mock_slides):
    mock_agent_state['slide_content'] = mock_slides
    mock_agent_state['topic'] = "Test PPT"
    
    with patch('agents.ppt_builder_agent.create_presentation') as mock_create:
        mock_create.return_value = "/path/to/Test_PPT_presentation.pptx"
        
        result = ppt_builder_agent(mock_agent_state)
        
        assert result['final_ppt_path'] == "/path/to/Test_PPT_presentation.pptx"
        mock_create.assert_called_once()
