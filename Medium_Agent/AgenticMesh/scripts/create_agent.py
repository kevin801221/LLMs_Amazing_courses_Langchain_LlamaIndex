# scripts/create_agent.py
import asyncio
from src.agent.intelligent_agent import IntelligentAgent

async def main():
    # 創建代理實例
    agent = IntelligentAgent(
        name="TestAgent",
        purpose="Testing and Development",
        capabilities=["planning", "analysis"]
    )
    
    # 註冊代理
    success = await agent.register()
    
    if success:
        print("Agent registered successfully!")
        # 測試任務規劃
        steps = await agent.plan_task(
            "分析一個數據集並生成報告"
        )
        print("\nTask Planning Steps:")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")

if __name__ == "__main__":
    asyncio.run(main())