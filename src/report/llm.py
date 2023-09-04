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

import yaml
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from dotenv import load_dotenv

load_dotenv("./.env", override=True, verbose=True)
with open("./conf/llmconfig.yaml", "r", encoding="utf-8") as f:
    llmconfig = yaml.safe_load(f)


class Chatbot:
    # TODO: Docstrings
    def __init__(self):
        self.function_llm = ChatOpenAI(**llmconfig["FUNCTIONLLM"])

        self.review_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=(llmconfig["ANALYSTPROMPT"])),
                HumanMessagePromptTemplate.from_template("Data : {data}"),
            ]
        )
        self.review_chain = LLMChain(
            llm=self.function_llm, prompt=self.review_prompt, verbose=True
        )

    def review_data(self, data):
        return self.review_chain.run(data=data)
