from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core import database
from app.api import deps
from app.models.company import Company
from app.models.financial_statement import FinancialStatement
from app.schemas.financial_statement import FinancialStatement as FinancialStatementSchema
from app.services import processing
from datetime import datetime

router = APIRouter()

@router.post("/upload/{company_id}", response_model=FinancialStatementSchema)
async def upload_financial_data(
    company_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    company = db.query(Company).filter(Company.id == company_id, Company.owner_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Placeholder for processing logic
    # In a real implementation, we would pass file.file to a processing service
    content = await file.read()
    processed_data = processing.process_file(content, file.filename)
    
    # Create DB entry
    statement = FinancialStatement(
        company_id=company_id,
        period_start=datetime.now().date(), # Stub date
        period_end=datetime.now().date(),   # Stub date
        statement_type="profit_loss",
        data=processed_data
    )
    db.add(statement)
    db.commit()
    db.refresh(statement)
    return statement

@router.get("/{company_id}", response_model=List[FinancialStatementSchema])
def read_financial_statements(
    company_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    company = db.query(Company).filter(Company.id == company_id, Company.owner_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company.financial_statements
