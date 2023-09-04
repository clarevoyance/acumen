import os
import pytest
from unittest.mock import patch, Mock, MagicMock
from src.chatbot import save_key, launch

class TestSaveKey:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.filename = '.test_env'

        yield  # this is where the testing happens

        # Teardown: Clean up the test file and directory after testing
        os.remove(self.filename)

    def test_save_key_file_exists(self):
        save_key('test_key', self.filename)
        assert os.path.isfile(self.filename) == True
        
    def test_save_key_string_value(self):
        save_key('test_key', self.filename)
        with open(self.filename) as f:
            my_key = f.read()
            assert my_key == "OPENAI_API_KEY='test_key'\n"
            

class TestLaunch():

    @patch('src.chatbot.os.getenv')
    @patch('src.chatbot.create_api_key_interface')
    def test_no_api_key_launches_interface(self, mock_create_api_key_interface, mock_getenv):
        mock_getenv.return_value = None
        mock_interface = Mock()
        mock_create_api_key_interface.return_value = mock_interface
        mock_interface.launch = Mock()

        launch()

        mock_create_api_key_interface.assert_called_once()
        mock_interface.launch.assert_called_once()

    @patch('src.chatbot.os.getenv')
    @patch('src.chatbot.DEV_CONFIG', {'test_all_prompts': False})
    @patch('src.run_prompts.run_all_prompts', create=True)
    @patch('src.chatbot.gr.ChatInterface')
    def test_api_key_and_test_all_prompts_false(self, mock_gr_interface, mock_run_all_prompts, mock_getenv):
        mock_getenv.return_value = 'some_api_key'

        launch()

        mock_run_all_prompts.assert_not_called()
        mock_gr_interface.assert_called_once()
        
    
    @patch('src.chatbot.os.getenv')
    @patch('src.chatbot.DEV_CONFIG', {'test_all_prompts': True})
    @patch('src.run_prompts.run_all_prompts', create=True)
    @patch('src.chatbot.gr.ChatInterface')
    def test_api_key_and_test_all_prompts_true(self, mock_gr_interface, mock_run_all_prompts, mock_getenv):
        """
        Test the launch function when API key is set and DEV_CONFIG['test_all_prompts'] is True.
        """
        mock_getenv.return_value = 'some_api_key'
        mock_gr_interface.return_value = MagicMock()
        mock_gr_interface.return_value.launch = MagicMock()

        launch()

        mock_run_all_prompts.assert_called_once()
        mock_gr_interface.assert_called_once()  # Check if gr.ChatInterface was called
        mock_gr_interface.return_value.launch.assert_called_once()  # Check if launch() method on the returned object was called