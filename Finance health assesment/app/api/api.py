from fastapi import APIRouter
from app.api.endpoints import auth, users, financials, assessments, companies

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(financials.router, prefix="/financials", tags=["financials"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
