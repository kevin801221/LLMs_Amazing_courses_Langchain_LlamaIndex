from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import time
import os
from dotenv import load_dotenv

# chat = Ollama(
#         model = "openchat:latest",
#         temperature=0
#     )

load_dotenv()

# chat = ChatOpenAI(
#     model = "gpt-3.5-turbo",
#     temperature=0.1,
#     api_key=os.environ.get("OPENAI_API_KEY"),
#     base_url=os.environ.get("OPENAI_BASE_URL")
# )

chat = ChatGroq(
    model="llama3-70b-8192",
    temperature=0.1
)

def stream(llm):

    chat = llm

    start_time = time.time()

    sysytem = "你是一個友好的人工助理。最重要的是，你總會用中文思考和回覆用戶的問題"
    human = "寫一首讚美{topic}的中文歌曲， 不少於1000字"

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", sysytem),
            ("human", human)
        ]
    )

    chain = prompt | chat #LCEL
    query = chain.invoke({
        "topic": "月餅"
    })

    print(query.content)

    end_time = time.time()
    print(f"該模型花了{end_time - start_time}秒")

stream(chat)