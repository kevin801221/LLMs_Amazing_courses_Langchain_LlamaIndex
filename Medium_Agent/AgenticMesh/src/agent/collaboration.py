# src/agent/collaboration.py
from typing import List, Dict
from .base import BaseAgent

class CollaborativeAgent(BaseAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collaborators: Dict[str, dict] = {}
        
    async def find_collaborators(self, required_capability: str):
        """尋找具有特定能力的協作者"""
        agents = await self.discover_agents(capability=required_capability)
        for agent in agents:
            if agent["agent_id"] not in self.collaborators:
                self.collaborators[agent["agent_id"]] = agent
        return list(self.collaborators.values())
        
    async def delegate_task(self, agent_id: str, task_data: dict):
        """委派任務給協作者"""
        if agent_id not in self.collaborators:
            return False
            
        agent = self.collaborators[agent_id]
        response = await self._make_request(
            "POST",
            f"{agent['endpoint']}/tasks",
            json=task_data
        )
        return response.status_code == 200