import os
import csv
import pytest
from unittest.mock import patch
from src.run_prompts import load_prompts, load_queries, write_output, run_all_prompts

class TestLoadPrompts:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.data_dir = 'test_data/'
        self.test_file = os.path.join(self.data_dir, 'test.txt')

        # Setup: Create a test directory and file for testing
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.test_file, 'w') as f:
            f.write('Test prompt')

        yield  # this is where the testing happens

        # Teardown: Clean up the test file and directory after testing
        os.remove(self.test_file)
        os.rmdir(self.data_dir)

    def test_load_prompts(self):
        prompts = load_prompts(self.data_dir)
        assert prompts == ['Test prompt']
        
        
    def test_load_prompts_no_txt_files(self):
        # Setup: Create a test directory with no .txt files
        empty_dir = 'test_data_empty/'
        os.makedirs(empty_dir, exist_ok=True)

        prompts = load_prompts(empty_dir)
        assert prompts == []

        # Teardown: Remove the test directory
        os.rmdir(empty_dir)


class TestLoadQueries:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.data_dir = 'test_data/'
        self.test_file = os.path.join(self.data_dir, 'queries.csv')

        # Setup: Create a test directory and file for testing
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.test_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Test query'])

        yield  # this is where the testing happens

        # Teardown: Clean up the test file and directory after testing
        os.remove(self.test_file)
        os.rmdir(self.data_dir)

    def test_load_queries(self):
        queries = load_queries(self.data_dir)
        assert queries == ['Test query']

    def test_load_queries_no_csv_files(self):
        # Setup: Create a test directory with no .csv files
        empty_dir = 'test_data_empty/'
        os.makedirs(empty_dir, exist_ok=True)

        with pytest.raises(FileNotFoundError):
            load_queries(empty_dir)

        # Teardown: Remove the test directory
        os.rmdir(empty_dir)
        
        
class TestWriteOutput:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.data_dir = 'test_data/'
        self.test_file = os.path.join(self.data_dir, 'output.csv')

        # Setup: Create a test directory for testing
        os.makedirs(self.data_dir, exist_ok=True)

        yield  # this is where the testing happens

        # Teardown: Clean up the test file and directory after testing
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.data_dir)

    def test_write_output_new_file(self):
        row = ['Test prompt', 'Test query', 'Test output', '']
        write_output(row, self.data_dir)

        with open(self.test_file, 'r', newline='') as f:
            reader = csv.reader(f)
            lines = list(reader)

        assert lines == [["prompt", "query", "output", "rating"], row]

    def test_write_output_existing_file(self):
        row1 = ['Test prompt 1', 'Test query 1', 'Test output 1', '']
        row2 = ['Test prompt 2', 'Test query 2', 'Test output 2', '']
        write_output(row1, self.data_dir)
        write_output(row2, self.data_dir)

        with open(self.test_file, 'r', newline='') as f:
            reader = csv.reader(f)
            lines = list(reader)

        assert lines == [["prompt", "query", "output", "rating"], row1, row2]
        
        
class TestRunAllPrompts:
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.data_dir = 'test_data/'
        self.test_file = os.path.join(self.data_dir, 'output.csv')

        # Setup: Create a test directory for testing
        os.makedirs(self.data_dir, exist_ok=True)

        yield  # this is where the testing happens

        # Teardown: Clean up the test file and directory after testing
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.data_dir)

    @patch('src.run_prompts.load_prompts')
    @patch('src.run_prompts.load_queries')
    @patch('src.run_prompts.run_chain')
    def test_run_all_prompts(self, mock_run_chain, mock_load_queries, mock_load_prompts):
        # Setup: Mock functions to return predictable results
        mock_load_prompts.return_value = ['prompt1', 'prompt2']
        mock_load_queries.return_value = ['query1', 'query2']
        mock_run_chain.return_value = 'output'

        run_all_prompts(self.data_dir)

        # Check if output.csv was created and contains the expected data
        with open(self.test_file, 'r', newline='') as f:
            reader = csv.reader(f)
            lines = list(reader)

        expected_lines = [
            ["prompt", "query", "output", "rating"],
            ['prompt1', 'query1', 'output', ''],
            ['prompt1', 'query2', 'output', ''],
            ['prompt2', 'query1', 'output', ''],
            ['prompt2', 'query2', 'output', ''],
        ]
        assert lines == expected_lines