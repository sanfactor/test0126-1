from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class VoteOption(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    ABSTAIN = "abstain"

class AgentRole(str, Enum):
    MARKET_ANALYST = "market_analyst"
    SECURITY_EXPERT = "security_expert"
    TOKEN_ECONOMIST = "token_economist"
    COMPLIANCE_SPECIALIST = "compliance_specialist"
    GOVERNANCE_EXPERT = "governance_expert"
    RISK_ASSESSOR = "risk_assessor"
    INFRASTRUCTURE_ANALYST = "infrastructure_analyst"
    MEMECOIN_STRATEGIST = "memecoin_strategist"
    ECOSYSTEM_EVALUATOR = "ecosystem_evaluator"

class Message(BaseModel):
    agent_id: str
    content: str
    timestamp: datetime
    role: AgentRole

class Vote(BaseModel):
    agent_id: str
    choice: VoteOption
    reasoning: str
    timestamp: datetime

class Discussion(BaseModel):
    id: str
    topic: str
    status: str
    messages: List[Message] = []
    votes: List[Vote] = []
    created_at: datetime
    updated_at: datetime
    conclusion: Optional[str] = None
