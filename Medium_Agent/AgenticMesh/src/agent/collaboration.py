# src/agent/collaboration.py
from typing import List, Dict
from .base import BaseAgent
from ..common.logging import agent_logger

class CollaborativeAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collaborators: Dict[str, dict] = {}
        
    async def find_collaborators(self, required_capability: str):
        """尋找具有特定能力的協作者"""
        try:
            # 記錄搜尋開始
            agent_logger.log_agent_action(
                "find_collaborators_start",
                {"required_capability": required_capability}
            )
            
            agents = await self.discover_agents(capability=required_capability)
            
            for agent in agents:
                if agent["agent_id"] not in self.collaborators:
                    self.collaborators[agent["agent_id"]] = agent
                    # 記錄新協作者
                    agent_logger.log_collaboration(
                        agent["agent_id"],
                        "collaborator_found",
                        "added",
                        {
                            "name": agent["name"],
                            "capabilities": agent["capabilities"]
                        }
                    )
            
            # 記錄搜尋結果
            agent_logger.log_agent_action(
                "find_collaborators_complete",
                {
                    "required_capability": required_capability,
                    "found_count": len(agents)
                }
            )
            
            return list(self.collaborators.values())
            
        except Exception as e:
            # 記錄錯誤
            agent_logger.log_error(
                "find_collaborators_error",
                str(e),
                {"required_capability": required_capability}
            )
            raise
        
    async def delegate_task(self, agent_id: str, task_data: dict):
        """委派任務給協作者"""
        try:
            if agent_id not in self.collaborators:
                agent_logger.log_error(
                    "delegate_task_error",
                    "Agent not found in collaborators",
                    {"agent_id": agent_id}
                )
                return False
                
            agent = self.collaborators[agent_id]
            
            # 記錄任務委派開始
            agent_logger.log_collaboration(
                agent_id,
                "task_delegation_start",
                "pending",
                task_data
            )
            
            response = await self._make_request(
                "POST",
                f"{agent['endpoint']}/tasks",
                json=task_data
            )
            
            success = response.status_code == 200
            
            # 記錄任務委派結果
            agent_logger.log_collaboration(
                agent_id,
                "task_delegation_complete",
                "success" if success else "failed",
                {
                    "task_data": task_data,
                    "response_status": response.status_code,
                    "response_body": response.json() if success else None
                }
            )
            
            return success
            
        except Exception as e:
            # 記錄錯誤
            agent_logger.log_error(
                "delegate_task_error",
                str(e),
                {
                    "agent_id": agent_id,
                    "task_data": task_data
                }
            )
            raise