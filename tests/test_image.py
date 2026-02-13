import pytest
from unittest.mock import patch, MagicMock
from agents.image.agent import image_agent

@pytest.fixture(autouse=True)
def mock_retry_settings():
    """Disable tenacity retries during tests."""
    with patch('agents.image.service.api_retry', lambda x: x):
        yield

def test_image_agent_no_slides(mock_agent_state):
    result = image_agent(mock_agent_state)
    assert result['slide_content'] == []

def test_image_agent_success(mock_agent_state, mock_slides):
    mock_agent_state['slide_content'] = mock_slides
    
    with patch('agents.image.service.ChatGroq') as MockLLM, \
         patch('agents.image.agent.fetch_image_url') as MockFetch:
        
        # Mock keyword generation logic (chain invoke)
        # Since chain is buried, let's rely on the loop structure.
        # But we can't easily mock the chain.invoke return value.
        # We CAN mock `fetch_image_url`.
        
        MockFetch.return_value = "http://mocked-url.com/img.jpg"
        
        # We need to ensure chain.invoke doesn't crash.
        # Mock ChatGroq to return a loose mock that doesn't fail on __or__.
        mock_llm_instance = MagicMock()
        MockLLM.return_value = mock_llm_instance
        
        # Patching ChatPromptTemplate
        with patch('agents.image.service.ChatPromptTemplate.from_template') as MockPrompt:
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = "test_keyword"
            
            # Simulate the piping behavior: prompt | llm | output_parser
            # We can mock the result of the piping operations? 
            # In Python, `|` is `__or__`.
            # If we make `MockPrompt.return_value` have an `__or__` that returns something...
            
            mock_prompt_instance = MagicMock()
            MockPrompt.return_value = mock_prompt_instance
            mock_prompt_instance.__or__.return_value.__or__.return_value = mock_chain
            
            # Run agent
            result = image_agent(mock_agent_state)
            
            # Assertions
            slides = result['slide_content']
            assert len(slides) == 2
            assert slides[0]['image_keyword'] == "test_keyword"
            assert slides[0]['image_url'] == "http://mocked-url.com/img.jpg"
