import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from langchain_core.output_parsers import StrOutputParser

from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser

load_dotenv()

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model = ChatGroq(
    model="llama3-70b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.9
)
# chain = prompt | model

# ai_reply = chain.invoke({"topic": "lions"})
# print(type(ai_reply))
# print(ai_reply.content)

# output_parser = StrOutputParser()

# chain = prompt | model | output_parser

# ai_reply = chain.invoke({"topic": "lions"})
# print(type(ai_reply))
# print(ai_reply)

# OpenAI Function Calling

class Joke(BaseModel):
    """Joke to tell user."""
    
    question: str = Field(description="question to set up a joke")
    answer: str = Field(description="answer to resolve the joke")
    
openai_functions = [convert_to_openai_function(Joke)]

json_parser = JsonOutputFunctionsParser()
chain = prompt | model.bind(functions=openai_functions) | json_parser
# ai_reply = chain.invoke({"topic": "lions"})
# print(type(ai_reply))
# print(ai_reply)

for sentence in chain.stream({"topic": "cats"}):
    print(sentence)