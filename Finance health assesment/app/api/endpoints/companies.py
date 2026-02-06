from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import database
from app.api import deps
from app.models.company import Company
from app.schemas.company import Company as CompanySchema, CompanyCreate

router = APIRouter()

@router.get("/", response_model=List[CompanySchema])
def read_companies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve companies owned by the current user.
    """
    companies = db.query(Company).filter(Company.owner_id == current_user.id).offset(skip).limit(limit).all()
    return companies

@router.post("/", response_model=CompanySchema)
def create_company(
    *,
    db: Session = Depends(database.get_db),
    company_in: CompanyCreate,
    current_user = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new company.
    """
    company = Company(
        name=company_in.name,
        industry=company_in.industry,
        owner_id=current_user.id,
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company
