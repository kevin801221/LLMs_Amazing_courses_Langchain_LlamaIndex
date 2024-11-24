# scripts/test_config.py
import os
import sys

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.common.config import get_settings

def test_settings():
    try:
        settings = get_settings()
        print("\n=== Configuration Settings ===")
        print(f"App Name: {settings.APP_NAME}")
        print(f"Debug Mode: {settings.DEBUG}")
        print(f"Default LLM Provider: {settings.DEFAULT_LLM_PROVIDER}")
        print(f"OpenAI API Key: {'Set' if settings.OPENAI_API_KEY else 'Not Set'}")
        print(f"Anthropic API Key: {'Set' if settings.ANTHROPIC_API_KEY else 'Not Set'}")
        print(f"Registry Host: {settings.REGISTRY_HOST}")
        print(f"Registry Port: {settings.REGISTRY_PORT}")
        print("===========================\n")
    except Exception as e:
        print(f"Error loading settings: {e}")
        raise

if __name__ == "__main__":
    test_settings()