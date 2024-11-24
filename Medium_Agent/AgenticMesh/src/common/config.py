# src/common/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """應用程式設定"""
    # 基本設定
    APP_NAME: str = "Agentic Mesh"
    DEBUG: bool = False
    
    # LLM設定
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    DEFAULT_LLM_PROVIDER: str = "anthropic"  # 或 "openai"
    
    # LLM模型設定
    OPENAI_MODEL: str = "gpt-4"
    ANTHROPIC_MODEL: str = "claude-3-opus-20240229"
    
    # LLM參數設定
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    
    # 註冊中心設定
    REGISTRY_HOST: str = "localhost"
    REGISTRY_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # 允許從額外的環境變量加載
        extra = "ignore"

@lru_cache()
def get_settings():
    """獲取設定單例"""
    return Settings()