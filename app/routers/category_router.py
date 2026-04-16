from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.response import success_response, error_response
from app.core.auth import get_current_user
from app.constants.messages import Messages

router = APIRouter(prefix="/categories", tags=["Categories"])

service = CategoryService()

@router.post("")
def create_category(data: CategoryCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    category= service.create_category(db, data)
    return success_response(category, Messages.CATEGORY_CREATED)

@router.get("")
def get_all_categories(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    categories = service.get_all_categories(db)
    return success_response(categories, Messages.CATEGORY_FETCHED)


@router.put("/{category_id}")
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    category = service.get_category_by_id(db, category_id)
    if not category:
        return error_response(Messages.CATEGORY_NOT_FOUND, 404)
    updated_category = service.update_category(db, category, data)
    return success_response(updated_category, Messages.CATEGORY_UPDATED)

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
        try:
            category = service.get_category_by_id(db, category_id)
            if not category:
               return error_response(Messages.CATEGORY_NOT_FOUND, 404)
            service.soft_delete_category(db, category)
            return success_response(Messages.CATEGORY_DELETED)
        except HTTPException as e:
            return error_response(e.detail, e.status_code)