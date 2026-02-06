from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import database
from app.api import deps
from app.models.company import Company
from app.models.assessment import Assessment
from app.schemas.assessment import Assessment as AssessmentSchema
from app.services import recommendation

router = APIRouter()

@router.post("/{company_id}/generate", response_model=AssessmentSchema)
def generate_assessment(
    company_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    company = db.query(Company).filter(Company.id == company_id, Company.owner_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Placeholder for AI Assessment logic
    # In a real app we'd fetch the latest financial statement here first
    # financial_data = db.query(FinancialStatement).filter(...).first().data
    financial_data = {"ratios": {"net_profit_margin": 0.15}} # Mock data for now
    
    result = recommendation.analyze_company_health(company, financial_data)
    
    # Create DB entry
    assessment = Assessment(
        company_id=company_id,
        overall_score=result["score"],
        risk_level=result["risk_level"],
        details=result
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment

@router.get("/{company_id}", response_model=List[AssessmentSchema])
def read_assessments(
    company_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    company = db.query(Company).filter(Company.id == company_id, Company.owner_id == current_user.id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return company.assessments
