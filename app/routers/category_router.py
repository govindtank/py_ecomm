from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.response import success_response, error_response

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


@router.put("/{category_id}")
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    category = service.get_category_by_id(db, category_id)
    if not category:
        return error_response("Category not found", 404)
    updated_category = service.update_category(db, category, data)
    return success_response(updated_category, "Category updated successfully")

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session= Depends(get_db)):
    category = service.get_category_by_id(db, category_id)
    if not category:
        return error_response("Category not found", 404)
    service.soft_delete_category(db, category)
    return success_response("Category deleted successfully")