
import pytest
from unittest.mock import patch, MagicMock
from agents.writer_agent import writer_agent

def test_writer_agent_no_outline(mock_agent_state):
    """Test writer returns empty if no outline."""
    mock_agent_state['presentation_outline'] = []
    result = writer_agent(mock_agent_state)
    assert result['slide_content'] == []

def test_writer_agent_error_handling(mock_agent_state):
    """Test graceful error handling."""
    mock_agent_state['presentation_outline'] = [{"title": "t", "description": "d"}]
    
    # Patch ChatGroq to return a mock that raises exception when invoked (or during chain execution)
    # But chain construction happens before try block.
    # We need to make chain.invoke fail.
    # Since we can't patch chain easily, let's patch JsonOutputParser to fail on get_format_instructions 
    # OR better: patch the invoke method of the LLM if usage was direct.
    
    with patch('agents.writer_agent.ChatGroq') as MockLLM:
        # Make the LLM instance compatible with the | operator
        mock_instance = MagicMock()
        MockLLM.return_value = mock_instance
        
        # We need the chain to fail on invoke.
        # The chain is prompt | llm | parser.
        # If any element in the chain raises, invoke raises.
        # Let's patch JsonOutputParser to raise on get_format_instructions which is called inside the try block
        with patch('agents.writer_agent.JsonOutputParser') as MockParser:
             mock_parser_instance = MagicMock()
             MockParser.return_value = mock_parser_instance
             mock_parser_instance.get_format_instructions.side_effect = Exception("LLM Fail")
             
             result = writer_agent(mock_agent_state)
             # Should return empty list on exception
             assert result['slide_content'] == []
