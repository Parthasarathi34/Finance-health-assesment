from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Company(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    industry = Column(String, index=True)
    tax_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="companies")
    financial_statements = relationship("FinancialStatement", back_populates="company")
    assessments = relationship("Assessment", back_populates="company")
