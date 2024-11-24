# scripts/test_intelligent_agent.py
import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agent.intelligent_agent import IntelligentAgent
from src.common.logging import agent_logger

class TestOutputManager:
    def __init__(self, log_dir: str = "test_outputs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.test_results = {
            "start_time": datetime.now().isoformat(),
            "agent_responses": [],
            "test_phases": {}
        }
    
    def add_agent_response(self, phase: str, task: str, response: dict):
        """記錄代理回應"""
        self.test_results["agent_responses"].append({
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "task": task,
            "response": response
        })
    
    def add_phase_result(self, phase: str, result: dict):
        """記錄測試階段結果"""
        self.test_results["test_phases"][phase] = {
            "timestamp": datetime.now().isoformat(),
            **result
        }
    
    def save_results(self):
        """保存測試結果"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = self.log_dir / f"test_results_{timestamp}.json"
        
        self.test_results["end_time"] = datetime.now().isoformat()
        
        with output_file.open('w', encoding='utf-8') as f:
            json.dump(self.test_results, f, ensure_ascii=False, indent=2)
        
        print(f"\nTest results saved to: {output_file}")

# 創建輸出管理器
output_manager = TestOutputManager()

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
    output_manager.add_phase_result("registration", {
        "planner": {"success": success}
    })
    
    print("\nRegistering AnalystAgent...")
    success = await analyst.register()
    output_manager.add_phase_result("registration", {
        "analyst": {"success": success}
    })
    
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
        
        # 紀錄代理回應
        output_manager.add_agent_response(
            phase="task_planning",
            task=task,
            response={"steps": steps}
        )
        
        # 輸出到終端
        print("\nGenerated steps:")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")

async def test_collaboration(agent: IntelligentAgent):
    """測試協作者查找"""
    print("\n=== Testing Collaboration ===")
    
    capabilities = ["analysis", "reporting", "planning"]
    
    for capability in capabilities:
        print(f"\nSearching for collaborators with {capability} capability...")
        collaborators = await agent.find_collaborators(required_capability=capability)
        
        # 記錄結果
        output_manager.add_phase_result(f"collaboration_{capability}", {
            "found_count": len(collaborators),
            "collaborators": [
                {
                    "name": c["name"],
                    "purpose": c["purpose"],
                    "capabilities": c["capabilities"]
                }
                for c in collaborators
            ]
        })
        
        # 輸出到終端
        if collaborators:
            print(f"Found {len(collaborators)} collaborators:")
            for collab in collaborators:
                print(f"- {collab['name']}: {collab['purpose']}")
                print(f"  Capabilities: {', '.join(collab['capabilities'])}")
        else:
            print(f"No collaborators found with {capability} capability")

async def main():
    """主測試流程"""
    start_time = datetime.now()
    print(f"Starting tests at {start_time}")
    
    try:
        planner, analyst = await test_agent_registration()
        await test_task_planning(planner)
        await test_collaboration(planner)
        
        # 測試複雜場景
        print("\n=== Testing Complex Scenario ===")
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
        
        # 記錄複雜任務結果
        output_manager.add_agent_response(
            phase="complex_task",
            task="data_analysis_project",
            response={"steps": steps}
        )
        
        # 輸出到終端
        print("\nComplex task execution plan:")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")
            
    except Exception as e:
        print(f"\nError during testing: {e}")
        raise
    finally:
        output_manager.save_results()
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