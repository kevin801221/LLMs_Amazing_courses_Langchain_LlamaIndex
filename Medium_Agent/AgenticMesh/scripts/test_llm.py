# scripts/test_llm.py
import asyncio
from src.services.llm_service import llm_service

async def test_llm():
    prompt = "請幫我規劃一個簡單的數據分析專案的步驟。"
    
    print("Testing OpenAI GPT:")
    llm_service.provider = "openai"
    response_gpt = await llm_service.get_completion(prompt)
    print(response_gpt)
    
    print("\nTesting Anthropic Claude:")
    llm_service.provider = "anthropic"
    response_claude = await llm_service.get_completion(prompt)
    print(response_claude)

if __name__ == "__main__":
    asyncio.run(test_llm())