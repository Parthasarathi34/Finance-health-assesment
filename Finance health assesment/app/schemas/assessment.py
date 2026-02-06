from pydantic import BaseModel
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AssessmentBase(BaseModel):
    overall_score: float
    risk_level: RiskLevel
    details: Dict[str, Any]

class AssessmentCreate(AssessmentBase):
    company_id: int

class Assessment(AssessmentBase):
    id: int
    company_id: int
    created_at: datetime

    class Config:
        from_attributes = True
