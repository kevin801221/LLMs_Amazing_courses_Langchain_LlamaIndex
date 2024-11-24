# src/registry/models.py
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

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