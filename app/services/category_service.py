from sqlalchemy.orm import Session
from app.repository.category_repo import CategoryRepository

repo = CategoryRepository()

class CategoryService:
    def create_category(self, db: Session, data):
        return repo.create_category(db, data)

    def get_all_categories(self, db: Session):
        return repo.get_all_categories(db)

    def get_category_by_id(self, db: Session, category_id : int):
        return repo.get_category_by_id(db, category_id)

    def update_category(self, db: Session, category, data):
        return repo.update_category(db, category, data)

    def soft_delete_category(self, db: Session, category):
        return repo.soft_delete_category(db, category)