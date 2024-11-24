# src/agent/base.py
from typing import List, Optional
import requests
from datetime import datetime

class BaseAgent:
    def __init__(self, name: str, purpose: str, capabilities: List[str]):
        self.name = name
        self.purpose = purpose
        self.capabilities = capabilities
        self.agent_id = None
        self.registry_url = "http://localhost:8000"
        
    async def register(self):
        """註冊至註冊中心"""
        registration_data = {
            "name": self.name,
            "purpose": self.purpose,
            "capabilities": self.capabilities,
            "endpoint": f"http://localhost:{self._get_port()}",
            "owner": "system",
            "policies": {}
        }
        
        response = await self._make_request(
            "POST",
            f"{self.registry_url}/register",
            json=registration_data
        )
        
        if response.status_code == 200:
            self.agent_id = response.json()["agent_id"]
            return True
        return False
        
    async def discover_agents(self, capability: Optional[str] = None):
        """發現其他代理"""
        params = {"capability": capability} if capability else {}
        response = await self._make_request(
            "GET",
            f"{self.registry_url}/agents",
            params=params
        )
        return response.json() if response.status_code == 200 else []