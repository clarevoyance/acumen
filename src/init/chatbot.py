import os
import gradio as gr
from dotenv import load_dotenv
from src.init.config import CONFIG, DEV_CONFIG
import csv


def write_output(prompt_id, query, output, data_dir="data/"):
    """Save output.csv with the columns prompt_id, query, output, rating"""

    # TODO: Write output is used twice, once in chatbot.py and once in run_prompts.py, with slight differences. can this be refactored?

    if not os.path.exists(data_dir + "output.csv"):
        with open(data_dir + "output.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["prompt_id", "query", "output", "rating"])
            writer.writerow([prompt_id, query, output, ""])
    else:
        with open(data_dir + "output.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([prompt_id, query, output, ""])


def predict(message, history):

    # Load the prompt from the path specified in the config file
    from src.init.chains import run_chain

    with open(CONFIG["default_prompt_path"], "r") as file:
        reader = csv.DictReader(file)
        prompt_id = str(CONFIG["default_prompt_id"])
        for row in reader:
            if row["id"] == prompt_id:
                prompt = row["prompt"]
        print(prompt)
    gpt_response = run_chain(prompt, message)
    write_output(prompt_id, message, gpt_response)

    return gpt_response


def save_key(api_key, filename=".env"):
    """if .env file does not exist, create one, else add to it"""
    if not os.path.exists(".env"):
        with open(filename, "w") as f:
            f.write(f"OPENAI_API_KEY='{api_key}'\n")
    else:
        with open(filename, "a") as f:
            f.write(f"OPENAI_API_KEY='{api_key}'\n")

    return "API Key saved successfully! Please restart the server."


def create_api_key_interface():
    with gr.Blocks() as interface:
        gr.Markdown("Enter your OpenAI API Key below and then click Save to save it")
        with gr.Row():
            inp = gr.Textbox(
                label="API Key", placeholder="Enter your OpenAI API Key here"
            )

        with gr.Row():
            out = gr.Markdown()

        btn = gr.Button("Save")
        btn.click(fn=save_key, inputs=inp, outputs=out)

    return interface


def launch():
    # if OPENAI_API_KEY is not available, ask the user for it

    load_dotenv()  # take environment variables from .env.
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if openai_api_key is None:
        create_api_key_interface().launch()

    else:
        TEST_ALL_PROMPTS = DEV_CONFIG["test_all_prompts"]
        if TEST_ALL_PROMPTS:
            from src.init.run_prompts import run_all_prompts

            run_all_prompts()
        gr.ChatInterface(fn=predict).launch()
