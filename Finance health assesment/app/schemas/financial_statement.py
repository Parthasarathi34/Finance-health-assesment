from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import date
from enum import Enum

class StatementType(str, Enum):
    PL = "profit_loss"
    BS = "balance_sheet"
    CASHFLOW = "cash_flow"

class FinancialStatementBase(BaseModel):
    statement_type: StatementType
    period_start: date
    period_end: date
    data: Dict[str, Any]

class FinancialStatementCreate(FinancialStatementBase):
    pass

class FinancialStatement(FinancialStatementBase):
    id: int
    company_id: int

    class Config:
        from_attributes = True
