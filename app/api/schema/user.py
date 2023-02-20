import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException


class UserBase(BaseModel):
    email: EmailStr
    password: str

    @validator("password", pre=True)
    def check_password(cls, v):
        if not re.match(
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d]{8,}$", v
        ):
            raise HTTPException(
                status_code=400,
                detail="Password must have a minimum of 8 characters, 1 Uppercase, 1 lowercase and 1 number",
            )
        return v


class UserCreateSchema(UserBase):
    pass


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class TokenResponseSchema(BaseModel):
    email: EmailStr
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: str
