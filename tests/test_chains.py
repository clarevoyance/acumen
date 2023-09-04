import pytest
from unittest.mock import patch, MagicMock
from src.chains import run_chain

# Mock CONFIG using pytest fixture
@pytest.fixture
def mock_config():
    with patch('src.chains.CONFIG', {'llm': 'gpt-3.5-turbo'}):
        yield

# Mock external classes and run test
@patch('src.chains.ChatOpenAI')
@patch('src.chains.LLMChain')
@patch('src.chains.PromptTemplate')
def test_run_chain(MockPromptTemplate, MockLLMChain, MockChatOpenAI, mock_config):
    # Mock the instances
    mock_llm_instance = MagicMock()
    mock_chain_instance = MagicMock()
    mock_prompt_instance = MagicMock()
    
    MockChatOpenAI.return_value = mock_llm_instance
    MockLLMChain.return_value = mock_chain_instance
    MockPromptTemplate.return_value = mock_prompt_instance
    
    # Mock the 'run' method to return a dummy output
    mock_chain_instance.run.return_value = "Mocked Output"
    
    # Now run the function
    prompt = "What is the capital of {}?"
    query = "France"
    output = run_chain(prompt, query)
    
    # Validate
    assert output == "Mocked Output"
    
    # You can also check if the mock instances were used correctly
    MockChatOpenAI.assert_called_once_with(temperature=1.0, model='gpt-3.5-turbo')
    MockPromptTemplate.assert_called_once_with(input_variables=["query"], template=prompt)
    MockLLMChain.assert_called_once_with(llm=mock_llm_instance, prompt=mock_prompt_instance)
    mock_chain_instance.run.assert_called_once_with(query)
