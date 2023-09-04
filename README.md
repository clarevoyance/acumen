# Acumen
Acumen enables developers to create smart applications based on their knowledge
base using a test-driven prompt engineering approach.

It allows an easy way to test your prompts automatically with minimal setup requirements.

## Setup

Create your environment with conda or venv
Run the following in your CLI to install all necessary requirements:
```
pip install -e .
```

## Verify
To verify this is properly installed run the following:
```bash
acumen
```

## Init
To initialize your application with example files:
```bash
acumen init
```
If this is your first time and/or no environment variable has been detected, you
will be prompted for your OpenAI API key. You can choose to create your own `.env`
file or simply enter the API key for your convenience.

The sample files `prompts.csv` and `queries.csv` will be created in the `/data` folder. 

## Run
To run the application:
```bash
acumen run
```
You will be able to run your application at http://127.0.0.1:7860 (default) or
the address specified in your cli upon running this command.

In the default setup, it is a simple haiku writer which you can modify in `data/prompts.csv`
The user queries in the app will send the LLM output based on the user input.
In this particular example, anything the user writes in their queries will always result
in a haiku based on their query.

## Advanced Features
Acumen allows for more advanced features such as recording a separate output file
showing the output of the user queries to allow for qualitative evaluation by a
domain expert.

Modify the `dev_config.yaml` file and set the `test_all_prompts` to `true` (false by default)

### Reporting Function (Under development)
We also have a reporting function which is still under development at this point
of time.

To run the report:
```bash
acumen report
```

You may use the sample `data/prompt_report.csv` to show a simple analysis of
the prompt testing results based on ratings from domain experts / user testing. 

This function is still under development and is not fully functional yet.
