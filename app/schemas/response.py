from pydantic import BaseModel
from typing import Optional, Any

class ApiResponse(BaseModel):
    success: bool
    statusCode: int
    message: str
    error: Optional[str]
    data: Optional[Any]

