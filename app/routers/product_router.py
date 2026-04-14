from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.product_service import ProductService
from app.schemas.product import ProductCreate, ProductUpdate
from app.utils.response import success_response, error_response


router= APIRouter(prefix="/products", tags=["Products"])

service = ProductService()

@router.post("")
def create_product(data : ProductCreate, db: Session = Depends(get_db)):
    product = service.create_product(db, data)
    return success_response(product, "Product created successfully")


@router.get("")
def get_products(
        page: int = 1,
        limit: int = 10,
        search: str = None,
        category_id : int = None,
        min_price : float = None,
        max_price : float = None,
        sort_by : str = None,
        order : str = 'asc',
        db: Session = Depends(get_db)
):
    filters=locals()
    products = service.get_products(db, filters)
    return success_response(products, "Products fetched successfully")


@router.get("/{product_id}")
def get_product_by_id(product_id : int, db: Session = Depends(get_db)):
    product = service.get_product_by_id(db, product_id)
    if not product:
        return error_response("Product not found", 404)
    return success_response(product, "Product fetched successfully")


@router.put("/{product_id}")
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    product = service.get_product_by_id(db, product_id)
    if not product:
        return error_response("Product not found", 404)
    updated_product = service.update_product(db, product, data)
    return success_response(updated_product, "Product updated successfully")


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = service.get_product_by_id(db, product_id)
    if not product:
        return error_response("Product not found", 404)
    service.soft_delete_product(db, product)
    return success_response("Product deleted successfully")