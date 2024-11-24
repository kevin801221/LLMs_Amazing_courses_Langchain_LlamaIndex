# src/agent/intelligent_agent.py
from typing import List, Dict, Optional
import asyncio
import aiohttp
from src.common.config import get_settings
from src.services.llm_service import llm_service

class IntelligentAgent:
    def __init__(
        self,
        name: str,
        purpose: str,
        capabilities: List[str],
        host: str = "localhost",
        port: int = 8001
    ):
        self.name = name
        self.purpose = purpose
        self.capabilities = capabilities
        self.endpoint = f"http://{host}:{port}"
        self.agent_id = None
        self.registry_url = "http://localhost:8000"
        self.settings = get_settings()
    
    async def register(self) -> bool:
        """註冊到註冊中心"""
        registration_data = {
            "name": self.name,
            "purpose": self.purpose,
            "capabilities": self.capabilities,
            "endpoint": self.endpoint,
            "owner": "system",
            "policies": {"max_runtime": "1h"}
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.registry_url}/register",
                json=registration_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.agent_id = data["agent_id"]
                    return True
                return False
    
    async def find_collaborators(
        self, 
        required_capability: Optional[str] = None
    ) -> List[Dict]:
        """尋找合適的協作者"""
        async with aiohttp.ClientSession() as session:
            params = {"capability": required_capability} if required_capability else {}
            async with session.get(
                f"{self.registry_url}/agents",
                params=params
            ) as response:
                if response.status == 200:
                    agents = await response.json()
                    # 排除自己
                    return [a for a in agents if a["agent_id"] != self.agent_id]
                return []
    
    async def plan_task(self, task_description: str) -> List[str]:
        """使用LLM規劃任務步驟"""
        prompt = f"""
        作為一個專業的任務規劃代理，請將以下任務分解為具體的執行步驟：
        
        任務：{task_description}
        
        請提供清晰的步驟列表，每個步驟都應該是具體且可執行的。
        """
        
        response = await llm_service.get_completion(
            prompt=prompt,
            system_prompt="你是一個專業的任務規劃助手。"
        )
        
        # 解析回應為步驟列表
        steps = [
            step.strip() 
            for step in response.split('\n') 
            if step.strip()
        ]
        return steps