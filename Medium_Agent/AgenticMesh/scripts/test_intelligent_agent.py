# scripts/test_intelligent_agent.py
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agent.intelligent_agent import IntelligentAgent

async def test_agent_registration():
    """測試代理註冊"""
    print("\n=== Testing Agent Registration ===")
    
    planner = IntelligentAgent(
        name="PlannerAgent",
        purpose="Task Planning and Coordination",
        capabilities=["planning", "coordination"],
        port=8001
    )
    
    analyst = IntelligentAgent(
        name="AnalystAgent",
        purpose="Data Analysis and Reporting",
        capabilities=["analysis", "reporting"],
        port=8002
    )
    
    # 註冊代理
    print("\nRegistering PlannerAgent...")
    success = await planner.register()
    print(f"PlannerAgent registration {'successful' if success else 'failed'}")
    
    print("\nRegistering AnalystAgent...")
    success = await analyst.register()
    print(f"AnalystAgent registration {'successful' if success else 'failed'}")
    
    return planner, analyst

async def test_task_planning(agent: IntelligentAgent):
    """測試任務規劃"""
    print("\n=== Testing Task Planning ===")
    
    test_tasks = [
        "分析過去一個月的銷售數據並製作報告",
        "為新產品開發制定項目時間表",
        "評估客戶滿意度調查結果"
    ]
    
    for task in test_tasks:
        print(f"\nPlanning task: {task}")
        steps = await agent.plan_task(task)
        print("Generated steps:")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")

async def test_collaboration(agent: IntelligentAgent):
    """測試協作者查找"""
    print("\n=== Testing Collaboration ===")
    
    # 測試不同能力的查找
    capabilities = ["analysis", "reporting", "planning"]
    
    for capability in capabilities:
        print(f"\nSearching for collaborators with {capability} capability...")
        collaborators = await agent.find_collaborators(required_capability=capability)
        
        if collaborators:
            print(f"Found {len(collaborators)} collaborators:")
            for collab in collaborators:
                print(f"- {collab['name']}: {collab['purpose']}")
                print(f"  Capabilities: {', '.join(collab['capabilities'])}")
        else:
            print(f"No collaborators found with {capability} capability")

async def main():
    """主測試流程"""
    print(f"Starting tests at {datetime.now()}")
    
    try:
        # 1. 測試代理註冊
        planner, analyst = await test_agent_registration()
        
        # 2. 測試任務規劃
        await test_task_planning(planner)
        
        # 3. 測試協作者查找
        await test_collaboration(planner)
        
        print("\n=== Additional Tests ===")
        
        # 4. 測試特定場景
        print("\nTesting complex scenario...")
        complex_task = """
        創建一個完整的數據分析項目：
        1. 收集銷售數據
        2. 清理和預處理數據
        3. 進行深入分析
        4. 生成視覺化報告
        5. 提供業務建議
        """
        
        print("\nPlanning complex task...")
        steps = await planner.plan_task(complex_task)
        print("\nComplex task execution plan:")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")
        
        # 5. 尋找具有多個能力的協作者
        print("\nSearching for specialized collaborators...")
        analysts = await planner.find_collaborators("analysis")
        if analysts:
            print("\nFound potential analysts for data processing:")
            for analyst in analysts:
                print(f"- {analyst['name']}")
                print(f"  Capabilities: {', '.join(analyst['capabilities'])}")
                print(f"  Purpose: {analyst['purpose']}")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        raise
    finally:
        print(f"\nTests completed at {datetime.now()}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"\nTest suite failed: {e}")
    finally:
        print("\nTest suite completed")