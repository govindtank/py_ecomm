from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.category import Category

class CategoryRepository:
    def create_category(self, db: Session, data):
        # Check if category already exists
        existing_category = db.query(Category).filter(
            Category.name == data.name,
            Category.is_deleted == False
        ).first()

        if existing_category:
            raise HTTPException(
                status_code=400,
                detail=f"Category '{data.name}' already exists"
            )

        category = Category(**data.dict())
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def get_all_categories(self, db: Session):
        return db.query(Category).all()

    def get_category_by_id(self, db: Session, category_id: int):
        return db.query(Category).filter(Category.id == category_id, Category.is_deleted == False).first()

    def update_category(self, db: Session, category, data):
        for key,value in data.dict(exclude_upset=True).items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
        return category

    def soft_delete_category(self, db: Session, category):
        category.is_deleted = True
        db.commit()
        # db.refresh(category)
        return category