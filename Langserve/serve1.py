#!/usr/bin/env python
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()
# 1. Create prompt template
system_template = "將以下內容翻譯成 {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])
# 2. Create model
model = ChatOpenAI(model=gpt-4)
# 3. Create parser
parser = StrOutputParser()
# 4. Create chain
chain = prompt_template | model | parser
# 5. App definition
app = FastAPI(
  title="LangChain 伺服器",
  version="1.0",
  description="使用 LangChain 的 Runnable 接口構建的簡單 API 伺服器",
)
# 5. Adding chain route
add_routes(
    app,
    chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)