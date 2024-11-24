# scripts/test_collaborative_agent.py
import asyncio
from src.agent.collaboration import CollaborativeAgent
from src.common.logging import agent_logger

async def main():
    # 創建協作代理
    agent = CollaborativeAgent(
        name="TestAgent",
        purpose="Testing collaboration",
        capabilities=["testing", "coordination"]
    )
    
    try:
        # 註冊代理
        await agent.register()
        agent_logger.log_agent_action(
            "agent_registration",
            {"name": agent.name, "agent_id": agent.agent_id}
        )
        
        # 尋找協作者
        collaborators = await agent.find_collaborators("analysis")
        
        # 如果找到協作者，委派任務
        if collaborators:
            for collaborator in collaborators:
                task_data = {
                    "task_type": "data_analysis",
                    "data": {"sample": "test_data"},
                    "priority": "high"
                }
                
                success = await agent.delegate_task(
                    collaborator["agent_id"],
                    task_data
                )
                
                agent_logger.log_agent_action(
                    "task_delegation_result",
                    {
                        "collaborator_id": collaborator["agent_id"],
                        "success": success
                    }
                )
                
    except Exception as e:
        agent_logger.log_error(
            "main_execution_error",
            str(e)
        )

if __name__ == "__main__":
    asyncio.run(main())