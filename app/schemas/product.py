from pydantic import BaseModel, Field
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., description="Name of the product", min_length=1)
    description: Optional[str] = Field(None, description="Description of the product")
    price: float = Field(..., description="Price of the product", gt=0)
    category_id: int

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name of the product", min_length=1)
    description: Optional[str] = Field(None, description="Description of the product")
    price: Optional[float] = Field(None, description="Price of the product", gt=0)
    category_id: Optional[int] = Field(None, description="ID of the category")