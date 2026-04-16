from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verify_password, create_access_token, get_password_hash
from app.models.user import User
from app.schemas.user import LoginRequest, TokenResponse
from app.utils.response import success_response, error_response
from app.constants.messages import Messages

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email, User.is_active == True).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail=Messages.INVALID_CREDENTIALS)
    
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(access_token=access_token)

# Seed endpoint to create first user (for testing)
@router.post("/seed-user")
def seed_user(db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.email == "admin@example.com").first()
        if existing:
            db.delete(existing)
            db.commit()
            db.flush()
        
        plain_password = "admin123"
        hashed_password = get_password_hash(plain_password)
        
        user = User(email="admin@example.com", password=hashed_password)
        db.add(user)
        db.commit()
        
        return success_response(
            {"email": "admin@example.com", "password": plain_password},
            Messages.USER_CREATED
        )
    except Exception as e:
        db.rollback()
        import traceback
        return error_response(f"{str(e)}\n{traceback.format_exc()}", 500)
