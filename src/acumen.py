# Copyright 2023 AI Singapore

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import click
from dotenv import load_dotenv, set_key
import gradio as gr
from src.init import demo, chatbot
from src.report.generate import process_csv


@click.group()
def cli():
    """Main CLI function that initializes commands."""
    pass


# @cli.command()
# def tutorial():
#     """
#     launches the tutorial page
#     """
#     pass


@cli.command()
def init():
    """Initializes Acumen by generating required files"""
    # Generate any required files from demo
    click.echo("Generating prompts and queries for demo app...")
    demo.generate_files()

    # Check if .env file exists
    if not os.path.exists(".env"):
        click.echo("no .env file found. Creating one now…")
        open(".env", "a").close()  # Create an empty .env file

        # Prompt the user for OpenAI API Key
        api_key = click.prompt(
            "Please enter your OpenAI API key or feel free to modify the .env file directly and press enter"
        )

        if api_key:  # If the user enters an API key, write it to .env
            set_key(".env", "OPENAI_API_KEY", api_key)
            click.echo(".env created with your API key. You may now `acumen run`")
        else:
            click.echo("You may now `acumen run`")
    else:
        click.echo("You may now `acumen run`")


@cli.command()
def run():
    """Runs the main application"""
    load_dotenv()  # Load .env variables
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        click.echo("Please set your OpenAI API key in the .env file before running.")
        return

    click.echo("Launching app...")
    chatbot.launch()


@cli.command()
def generate():
    """
    this generates the report in the specified format

    available formats: pdf, app
    """
    print("Generating PDF")


@cli.command()
def report():
    """Runs the prompt report functionality"""
    # Gradio interface
    with gr.Blocks(title="Acumen Report") as app:
        with gr.Row():
            with gr.Column():
                input_csv = gr.File(
                    label="Upload CSV", file_types=["csv", "xlsx"], interactive=True
                )
                df = gr.DataFrame(
                    headers=["prompt", "Prompts"], col_count=2
                )  # I want to pass in the csv file above
            with gr.Column():
                bar_plot = gr.Image()
                bar_plot_review = gr.Textbox()
                corr_plot = gr.Image()
                corr_review = gr.Textbox()

        input_csv.upload(
            fn=process_csv,
            inputs=input_csv,
            outputs=[df, bar_plot, bar_plot_review, corr_plot, corr_review],
        )

    app.launch()
