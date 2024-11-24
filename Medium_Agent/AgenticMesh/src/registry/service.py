# src/registry/service.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

app = FastAPI()

# 數據模型
class AgentRegistration(BaseModel):
    name: str
    purpose: str
    capabilities: List[str]
    endpoint: str
    owner: str
    policies: Dict[str, str]

class AgentMetadata(AgentRegistration):
    agent_id: str
    status: str
    registered_at: datetime
    last_active: datetime

# 內存存儲
agent_registry: Dict[str, AgentMetadata] = {}

@app.get("/")
async def root():
    return {"message": "Agentic Mesh Registry Service"}

@app.post("/register")
async def register_agent(registration: AgentRegistration):
    """註冊新代理"""
    from uuid import uuid4
    agent_id = str(uuid4())
    
    metadata = AgentMetadata(
        **registration.dict(),
        agent_id=agent_id,
        status="active",
        registered_at=datetime.now(),
        last_active=datetime.now()
    )
    
    agent_registry[agent_id] = metadata
    return {"agent_id": agent_id, "status": "registered"}

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """獲取代理信息"""
    if agent_id not in agent_registry:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent_registry[agent_id]

@app.get("/agents")
async def list_agents(capability: Optional[str] = None):
    """列出所有代理"""
    agents = list(agent_registry.values())
    if capability:
        agents = [
            agent for agent in agents 
            if capability in agent.capabilities
        ]
    return agents

@app.delete("/agents/{agent_id}")
async def deregister_agent(agent_id: str):
    """註銷代理"""
    if agent_id not in agent_registry:
        raise HTTPException(status_code=404, detail="Agent not found")
    del agent_registry[agent_id]
    return {"status": "deregistered"}