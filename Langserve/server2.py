#!/usr/bin/env python
from fastapi import FastAPI, HTTPException, Form, Body
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
import logging
from typing import List, Optional
from langdetect import detect
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key=os.getenv('OPENAI_API_KEY', 'YourAPIKey')
# 設置日誌記錄
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. 創建多語言翻譯提示模板
system_template = "將以下內容翻譯成 {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# 2. 創建模型
model = ChatOpenAI()

# 3. 創建解析器
parser = StrOutputParser()

# 4. 創建翻譯鏈
translation_chain = prompt_template | model | parser

# 5. App 定義
app = FastAPI(
    title="LangChain 增強版文字翻譯伺服器",
    version="2.0",
    description="使用 LangChain 的 Runnable 接口構建的多功能文字翻譯 API 伺服器",
)
# 根路徑處理
@app.get("/")
async def read_root():
    return {"message": "Welcome to the LangChain Translation API. Use /translate/ to access the translation service."}
# 6. 批量翻譯處理函數
async def handle_batch_translation(language: str, texts: List[str]) -> List[str]:
    results = []
    for text in texts:
        try:
            logger.info(f"翻譯文本: {text} -> {language}")
            result = await translation_chain.arun({"language": language, "text": text})
            logger.info(f"翻譯結果: {result}")
            results.append(result)
        except Exception as e:
            logger.error(f"翻譯過程中出現錯誤: {e}")
            raise HTTPException(status_code=500, detail=f"翻譯文本 '{text}' 時出現錯誤")
    return results

# 7. 翻譯語言檢測
def detect_language(text: str) -> str:
    try:
        detected_language = detect(text)
        logger.info(f"檢測到的語言: {detected_language}")
        return detected_language
    except Exception as e:
        logger.error(f"語言檢測失敗: {e}")
        raise HTTPException(status_code=500, detail="語言檢測失敗")

# 8. 翻譯路由
@app.post("/translate/")
async def translate(
    language: str = Form(...), 
    texts: Optional[List[str]] = Body(None),
    text: Optional[str] = Form(None),
    auto_detect: bool = Form(False)
):
    if texts:
        if auto_detect:
            detected_languages = [detect_language(t) for t in texts]
            return {"detected_languages": detected_languages, "translations": await handle_batch_translation(language, texts)}
        return await handle_batch_translation(language, texts)
    elif text:
        if auto_detect:
            detected_language = detect_language(text)
            return {"detected_language": detected_language, "translation": await handle_batch_translation(language, [text])}
        return {"translation": await handle_batch_translation(language, [text])}
    else:
        raise HTTPException(status_code=400, detail="必須提供至少一段文本進行翻譯")

# 9. 添加鏈路由
add_routes(
    app,
    translation_chain,
    path="/chain",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
