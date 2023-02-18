from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.cors.database import get_db
from app.api.schema import user
from app.db.models.users import User
from app.cors import security


router = APIRouter()


def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    return user


@router.post('/account/signup', response_model=user.UserResponseSchema, status_code=201)
async def create_user(user: user.UserCreateSchema, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail=f"email already exists")
    user.password = security.hash_password(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login', response_model=user.TokenResponseSchema)
async def login_user(user_in: user.LoginUserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        raise HTTPException(status_code=403, detail=f"Invalid Credentials")
    is_password_verified = security.verify_password(
        user_in.password, user.password)
    if is_password_verified == False:
        raise HTTPException(status_code=403, detail=f"Invalid Credentials")
    access_token = security.create_access_token(
        data={"user_id": user.id, "user_email": user.email})
    return {
        "email": user.email,
        "access_token": access_token,
        "token_type": "Bearer"
    }
