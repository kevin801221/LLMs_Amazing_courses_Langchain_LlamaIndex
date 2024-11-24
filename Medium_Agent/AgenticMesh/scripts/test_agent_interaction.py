# scripts/test_agent_interaction.py
import asyncio
from src.agent.intelligent_agent import IntelligentAgent

async def test_interaction():
    # 創建兩個代理
    planner = IntelligentAgent(
        name="PlannerAgent",
        purpose="Project Planning",
        capabilities=["planning", "coordination"]
    )
    
    analyst = IntelligentAgent(
        name="AnalystAgent",
        purpose="Data Analysis",
        capabilities=["analysis", "reporting"]
    )
    
    # 註冊代理
    await planner.register()
    await analyst.register()
    
    # 測試協作
    task = "創建一個完整的數據分析報告"
    
    # 讓規劃者制定計劃
    steps = await planner.plan_task(task)
    print("\nPlanned Steps:")
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")
    
    # 尋找合適的協作者
    collaborators = await planner.discover_agents()
    print("\nFound Collaborators:")
    for agent in collaborators:
        print(f"- {agent.name}: {agent.purpose}")

if __name__ == "__main__":
    asyncio.run(test_interaction())