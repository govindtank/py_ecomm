from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.response import success_response, error_response
from app.core.auth import get_current_user
from app.constants.messages import Messages


router= APIRouter(prefix="/products", tags=["Products"])

service = ProductService()

@router.post("")
def create_product(data: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    product = service.create_product(db, data)
    return success_response(product, Messages.PRODUCT_CREATED)


@router.get("")
def get_products(
        page: int = 1,
        limit: int = 10,
        search: str = None,
        category_id : int = None,
        category_name: str = None,
        min_price : float = None,
        max_price : float = None,
        sort_by : str = None,
        order : str = 'asc',
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    # filters=locals()
    filters = {
        "search": search,
        "category_id": category_id,
        "category_name": category_name,
        "min_price": min_price,
        "max_price": max_price,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit
    }
    products = service.get_products(db, filters)
    return success_response(products, Messages.PRODUCT_FETCHED)


@router.get("/{product_id}")
def get_product_by_id(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    product = service.get_product_by_id(db, product_id)
    if not product:
        return error_response(Messages.PRODUCT_NOT_FOUND, 404)
    return success_response(product, Messages.PRODUCT_FETCHED)


@router.put("/{product_id}")
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    product = service.get_product_by_id(db, product_id)
    if not product:
        return error_response(Messages.PRODUCT_NOT_FOUND, 404)
    updated_product = service.update_product(db, product, data)
    return success_response(updated_product, Messages.PRODUCT_UPDATED)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    product = service.get_product_by_id(db, product_id)
    if not product:
        return error_response(Messages.PRODUCT_NOT_FOUND, 404)
    service.soft_delete_product(db, product)
    return success_response(Messages.PRODUCT_DELETED)
