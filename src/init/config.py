import yaml
import os


def load_config(filename):
    # !: Need to change the path to the config file
    # Get the directory of the current file
    # current_directory = os.path.dirname(__file__)
    # Get the parent directory
    # parent_directory = os.path.dirname(current_directory)

    try:
        with open(filename, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        if filename == "config.yaml":
            print(
                "Configuration file not found. Run 'acumen init' to populate with example config, prompts, and queries."
            )
        else:
            print(f"Configuration file {filename} not found.")

        return None


CONFIG = load_config("config.yaml")
DEV_CONFIG = load_config("dev_config.yaml")
