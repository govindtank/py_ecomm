from sqlalchemy import Column, Integer, String, Boolean
from app.core.database import Base


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_deleted = Column(Boolean, default=False)
