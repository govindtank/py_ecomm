from pydantic import BaseModel, Field
from typing import Optional

class CategoryCreate(BaseModel):
    name: str = Field(..., description="Name of the category", min_length=1)

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the category", min_length=1)