from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain import PromptTemplate
from src.init.config import CONFIG


def run_chain(prompt, query):

    llm = ChatOpenAI(temperature=1.0, model=CONFIG["llm"])

    prompt = PromptTemplate(
        input_variables=["query"],
        template=prompt,
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    output = chain.run(query)
    return output
