from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    industry: Optional[str] = None
    tax_id: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
