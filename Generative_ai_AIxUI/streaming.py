import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnableParallel

load_dotenv()

# print(os.getenv("OPENAI_BASE_URL"))

# model = ChatOpenAI(
#     model="gpt-3.5-turbo",
#     api_key=os.getenv("OPENAI_API_KEY"),
#     base_url=os.getenv("OPENAI_BASE_URL"),
#     temperature=0.9
# )

model = ChatGroq(
    model="llama3-70b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.9
)

# Streaming

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")

output_parser = StrOutputParser()

chain1 = prompt | model | output_parser

# for sentence in chain.stream({"topic": "apple"}):
#     print(sentence)
    
prompt = ChatPromptTemplate.from_template("Write me a poem about {topic}")

chain2 = prompt | model | output_parser

paraller_chain = RunnableParallel({
    "joke": chain1,
    "poem": chain2
})

for sentence in paraller_chain.stream({"topic": "oranage"}):
    print(sentence)
    
result = {}
for sentence in paraller_chain.stream({"topic": "monkey"}):
    for key, value in sentence.items():
        if key not in result:
            result[key] = ""
        result[key] += value
        
    print(result)