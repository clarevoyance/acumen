import os
import pytest
import yaml
from src.config import load_config

class TestConfig:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        self.config_path = 'test_config.yaml'
        self.dev_config_path = 'test_dev_config.yaml'
        self.sample_config = {'key': 'value'}
        self.sample_dev_config = {'dev_key': 'dev_value'}
        
        with open(self.config_path, 'w') as f:
            yaml.dump(self.sample_config, f)
        
        with open(self.dev_config_path, 'w') as f:
            yaml.dump(self.sample_dev_config, f)

        yield  # This is where the testing happens

        # Teardown
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        if os.path.exists(self.dev_config_path):
            os.remove(self.dev_config_path)

    def test_load_config(self):
        config = load_config(self.config_path)
        assert config == self.sample_config

        dev_config = load_config(self.dev_config_path)
        assert dev_config == self.sample_dev_config

    def test_file_not_found(self):
        assert load_config('nonexistent_file.yaml') is None
