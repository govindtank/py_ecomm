from sqlalchemy.orm import Session
from app.repository.category_repo import CategoryRepository

repo = CategoryRepository()

class CategoryService:
    def create_category(self, db: Session, data):
        return repo.create_category(db, data)

    def get_all_categories(self, db: Session):
        return repo.get_all_categories(db)