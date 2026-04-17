from sqlalchemy.orm import Session
from app.repository.product_repo import ProductRepository
from app.models.product import Product
from app.models.category import Category

repo= ProductRepository()

class ProductService:
    def create_product(self, db: Session, data):
        return repo.create_product(db, data)

    def get_products(self, db: Session, filters):
        # query = db.query(Product).filter(Product.is_deleted == False)
        query = db.query(Product, Category.name.label("category_name")).join(Category).filter(
            Product.is_deleted==False, Category.is_deleted==False        )


        #search func
        if filters.get("search"):
            # query = db.query(Product).filter(Product.name.ilike(f"${filters['search']}%"))
            search_term = f"%{filters['search']}%"
            query = query.filter(Product.name.ilike(search_term))

        #catgory filter
        if filters.get("category_id"):
            query = query.filter(Product.category_id == filters['category_id'])
        elif filters.get("category_name"):
            query = query.join(Category).filter(
                Category.name.ilike(f"%{filters['category_name']}%"),
                Category.is_deleted == False)


            #price wise filter
        if filters.get("min_price"):
            query= query.filter(Product.price >= filters["min_price"])
        if filters.get("max_price"):
            query= query.filter(Product.price <= filters["max_price"])

        #sorting mechinsm
        if filters.get("sort_by"):
            valid_columns = ['id', 'name', 'price', 'created_at', 'description',  'category_id']
            sort_column = filters["sort_by"]

            if sort_column in valid_columns:
                column = getattr(Product, sort_column)

                if filters.get("order") == "desc":
                    column = column.desc()
                query = query.order_by(column)


        page = filters.get("page", 1)
        limit = filters.get("limit", 10)

        total = query.count()
        # items= query.offset((page-1)*limit).limit(limit).all()
        items=[]
        for product, category_name in query.offset((page-1)*limit).limit(limit).all():
            product_dict={
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price":product.price,
                "category_id":product.category_id,
                "category_name":category_name,
                "is_deleted":product.is_deleted,
                "created_at":product.created_at
            }
            items.append(product_dict)


        return{
            "total": total,
            "page":page,
            "limit":limit,
            "items": items
        }

    def get_product_by_id(self, db: Session, product_id : int):
        # return repo.get_product_by_id(db, product_id)
        result = (db.query(Product, Category.name.label("category_name")).join(Category)
                  .filter(Product.id ==product_id, Product.is_deleted==False, Category.is_deleted==False).first())

        if result:
            product, category_name=result
            return{
                "id":product.id,
                "name":product.name,
                "description":product.description,
                "price":product.price,
                "category_id":product.category_id,
                "category_name":category_name,
                "is_deleted":product.is_deleted,
                "created_at":product.created_at
            }
        return None

    def update_product(self, db, product, data):
        return repo.update_product(db, product, data)

    def soft_delete_product(self, db, product):
        return repo.soft_delete_product(db, product)