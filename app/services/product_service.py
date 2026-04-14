from sqlalchemy.orm import Session
from app.repository.product_repo import ProductRepository
from app.models.product import Product


repo= ProductRepository()

class ProductService:
    def create_product(self, db: Session, data):
        return repo.create_product(db, data)

    def get_products(self, db: Session, filters):
        query = db.query(Product).filter(Product.is_deleted == False)

        #search func
        if filters.get("search"):
            query = db.query(Product).filter(Product.name.ilike(f"${filters['search']}%"))

        #catgory filter
        if filters.get("category_id"):
            query = db.query(Product).filter(Product.category_id == filters['category_id'])

        #price wise filter
        if filters.get("min_price"):
            query= query.filter(Product.price >= filters["min_price"])
        if filters.get("max_price"):
            query= query.filter(Product.price <= filters["max_price"])

        #sorting mechinsm
        if filters.get("sort_by"):
            column= getattr(Product, filters["sort_by"])
            if filters.get("sort") == "desc":
                column = column.desc()
            query = query.order_by(column)

        page = filters.get("page", 1)
        limit = filters.get("limit", 10)

        total = query.count()
        items= query.offset((page-1)*limit).limit(limit).all()

        return{
            "total": total,
            "page":page,
            "limit":limit,
            "items": items
        }

    def get_product_by_id(self, db: Session, product_id : int):
        return repo.get_product_by_id(db, product_id)


    def update_product(self, db, product, data):
        return repo.update_product(db, product, data)

    def soft_delete_product(self, db, product):
        return repo.soft_delete_product(db, product)