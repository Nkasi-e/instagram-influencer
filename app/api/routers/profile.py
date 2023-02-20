
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.cors.database import get_db
from app.cors.security import get_current_user
from app.api.schema import profile
from app.db.models.users import Profile, User

router = APIRouter()


@router.post('/profile', response_model=profile.ProfileResponseSchema, status_code=201)
def create_profile(data_in: profile.ProfileCreate, db: Session = Depends(get_db), auth_user: User = Depends(get_current_user)):
    profile = Profile(owner_id=auth_user.id, **data_in.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
