# src/services/llm_service.py
from typing import Dict, Optional, Any
import anthropic
import openai
from ..common.config import get_settings

settings = get_settings()

class LLMService:
    """LLM服務封裝"""
    
    def __init__(self):
        self.provider = settings.DEFAULT_LLM_PROVIDER
        self._init_clients()
        
    def _init_clients(self):
        """初始化LLM客戶端"""
        if settings.ANTHROPIC_API_KEY:
            self.anthropic_client = anthropic.Anthropic(
                api_key=settings.ANTHROPIC_API_KEY
            )
        
        if settings.OPENAI_API_KEY:
            self.openai_client = openai.OpenAI(
                api_key=settings.OPENAI_API_KEY
            )
    
    async def get_completion(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """獲取LLM回應"""
        if self.provider == "anthropic":
            return await self._get_anthropic_completion(
                prompt, max_tokens, temperature, system_prompt
            )
        else:
            return await self._get_openai_completion(
                prompt, max_tokens, temperature, system_prompt
            )
    
    async def _get_anthropic_completion(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """使用Anthropic的Claude獲取回應"""
        message = self.anthropic_client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=max_tokens or settings.MAX_TOKENS,
            temperature=temperature or settings.TEMPERATURE,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content[0].text
    
    async def _get_openai_completion(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """使用OpenAI的GPT獲取回應"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = await self.openai_client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=max_tokens or settings.MAX_TOKENS,
            temperature=temperature or settings.TEMPERATURE
        )
        return response.choices[0].message.content

# 創建LLM服務單例
llm_service = LLMService()