from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum, JSON, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.models.base import Base

class StatementType(str, enum.Enum):
    PL = "profit_loss"
    BS = "balance_sheet"
    CASHFLOW = "cash_flow"

class FinancialStatement(Base):
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    statement_type = Column(String, nullable=False) # Use string to store enum value
    data = Column(JSON, nullable=False) # Stores the raw/processed financial data
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    company = relationship("Company", back_populates="financial_statements")
