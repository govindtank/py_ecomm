from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["john@example.com"])
    password: str = Field(..., examples=["strong_password"])

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "strong_password"
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

