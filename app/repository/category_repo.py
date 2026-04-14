from sqlalchemy.orm import Session
from app.models.category import Category

class CategoryRepository:
    def create_category(self, db: Session, data):
        category = Category(**data.dict())
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def get_all_categories(self, db: Session):
        return db.query(Category).all()