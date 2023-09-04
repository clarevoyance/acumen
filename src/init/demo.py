import os
import csv


def generate_files(
    data_dir="data/",
    prompts=[
        """You are a haiku chatbot. Generate a haiku given the user query. Make it cute. Query: {query}""",
        """You are a limerick bot. Compose a limerick based on the user's input. Query: {query}""",
        """You are a sonnet generator. Create a sonnet using the theme provided by the user. Theme: {query}"""
        """You are a joke bot. Generate a one-liner joke based on the user's topic. Topic: {query}"""
        """You are a motivational quote bot. Craft a motivational quote in response to the user's situation. Situation: {query}"""
        """You are a riddle bot. Create a riddle using the object mentioned by the user. Object: {query}"""
        """You are a recipe bot. Suggest a recipe based on the ingredients the user has. Ingredients: {query}"""
        """You are a tongue twister bot. Generate a tongue twister using the word provided by the user. Word: {query}"""
        """You are a flash fiction bot. Write a 100-word story based on the user's prompt. Prompt: {query}"""
        """You are a dialogue bot. Create a short dialogue between two characters based on the user's scenario. Scenario: {query}"""
        """You are a trivia bot. Generate a trivia question related to the user's interest. Interest: {query}"""
    ],
    queries=[["I want a fox haiku"], ["haiku about sharks"]],
    config_path="config.yaml",
):
    """Generate files with prompts and queries in the specified directory."""
    # Ensure the data directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Write the prompts to prompts.csv with a id col and a prompt col
    with open(os.path.join(data_dir, "prompts.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "prompt"])
        for i, prompt in enumerate(prompts):
            writer.writerow([i + 1, prompt])

    # Write the queries to queries.csv
    with open(os.path.join(data_dir, "queries.csv"), "w", newline="") as f:
        writer = csv.writer(f)
        for query in queries:
            writer.writerow(query)

    import yaml

    data = {
        "llm": "gpt-3.5-turbo-0613",
        "default_prompt_path": f"{data_dir}prompts.csv",
        "default_prompt_id": 1,
    }

    with open(config_path, "w") as file:
        yaml.dump(data, file, default_flow_style=False)
