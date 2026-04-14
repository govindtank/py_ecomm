from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate
from app.utils.response import success_response


router = APIRouter(prefix="/categories", tags=["Categories"])

service = CategoryService()

@router.post("")
def create_category(data : CategoryCreate, db: Session = Depends(get_db)):
    category= service.create_category(db, data)
    return success_response(category, "Category created successfully")

@router.get("")
def get_all_categories(db: Session = Depends(get_db)):
    categories = service.get_all_categories(db)
    return success_response(categories, "Categories fetched successfully")
