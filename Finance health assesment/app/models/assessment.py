from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, JSON, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base

class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Assessment(Base):
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    overall_score = Column(Float) # 0-100 or similar score
    risk_level = Column(String) # Store RiskLevel enum as string
    details = Column(JSON) # Detailed analysis, recommendations, etc.
    
    company = relationship("Company", back_populates="assessments")
