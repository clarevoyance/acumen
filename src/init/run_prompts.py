import csv
import os
from src.init.chains import run_chain


def load_prompts(data_dir="data/"):
    """Read all the prompts from the prompt.csv"""
    with open(data_dir + "prompts.csv", "r") as f:
        reader = csv.DictReader(f)
        prompts = [row for row in reader]
    return prompts


def load_queries(data_dir="data/"):
    """Read all the queries from queries.csv"""
    with open(data_dir + "queries.csv", "r") as f:
        reader = csv.reader(f)
        queries = [row[0] for row in reader]
        return queries


def write_output(row, data_dir="data/"):
    """Save output.csv with the columns prompt, query, output, rating"""
    if not os.path.exists(data_dir + "output.csv"):
        with open(data_dir + "output.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["prompt_id", "query", "output", "rating"])
            writer.writerow(row)
    else:
        with open(data_dir + "output.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(row)


def run_all_prompts(data_dir="data/"):
    """Run all the prompts with all the queries and save the output in output.csv"""
    prompts = load_prompts(data_dir)
    queries = load_queries(data_dir)
    for prompt in prompts:
        for query in queries:
            output = run_chain(prompt["prompt"], query)
            row = [prompt["id"], query, output, ""]
            write_output(row, data_dir)
