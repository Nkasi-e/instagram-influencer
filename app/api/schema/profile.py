from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr


class ProfileBase(BaseModel):
    username: constr(strip_whitespace=True)
    followers: int
    bio: Optional[constr(max_length=100)] = None


class ProfileCreate(ProfileBase):
    pass


class UserDetails(BaseModel):
    id: str
    email: str

    class Config:
        orm_mode = True


class ProfileResponseSchema(ProfileBase):
    id: int
    created_at: datetime
    owner: UserDetails

    class Config:
        orm_mode = True
