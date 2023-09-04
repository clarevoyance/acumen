import os
import csv
import pytest
from src.demo import generate_files

class TestGenerateFiles:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.data_dir = 'test_data/'
        self.config_path = 'test_config.yaml'

        yield  # this is where the testing happens

        # Teardown: Clean up the test files and directory after testing
        for filename in ['prompt1.txt', 'prompt2.txt', 'queries.csv']:
            file_path = os.path.join(self.data_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        if os.path.exists(self.data_dir):
            os.rmdir(self.data_dir)
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def test_generate_files(self):
        generate_files(data_dir=self.data_dir, config_path=self.config_path)

        # Check if the data directory was created
        assert os.path.isdir(self.data_dir)

        # Check if the prompt files were created and contain the expected data
        for i, expected_data in enumerate([
            """You are a storywriting chatbot. Generate a story given the user query. If no genre is specified, the genre should be fairy tale. If the age range is not specified, the story should be written for 7-9 year olds. If the story length is not specified, keep it to 500 words or less. Query: {query}""",
            """You are a storywriting chatbot. Generate a story given the user query. If no genre is specified, the genre should be thriller. If the age range is not specified, the story should be written for young adults. If the story length is not specified, keep it to 500 words or less. Query: {query}"""
        ], 1):
            file_path = os.path.join(self.data_dir, f'prompt{i}.txt')
            assert os.path.isfile(file_path)
            with open(file_path, 'r') as f:
                assert f.read() == expected_data

        # Check if the queries.csv file was created and contains the expected data
        file_path = os.path.join(self.data_dir, 'queries.csv')
        assert os.path.isfile(file_path)
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            lines = list(reader)
        assert lines == [["I want a story of a fox and a whale"], ["story about sharks"]]
        
        assert self.config_path == 'test_config.yaml'