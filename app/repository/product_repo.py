from sqlalchemy.orm import Session
from app.models.product import Product

class ProductRepository:

    def create_product(self, db: Session, data):
        product= Product(**data.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def get_all_products(self, db: Session, query):
        return query.all()

    def get_product_by_id(self, db: Session, product_id : int):
        return db.query(Product).filter(Product.id == product_id, Product.is_deleted == False).first()

    def update_product(self, db: Session, product, data):
        for key, value in data.dict(exclude_unset=True).items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
        return product

    def soft_delete_product(self, db: Session, product):
        product.is_deleted = True
        db.commit()
        # db.refresh(product)
        # return product
