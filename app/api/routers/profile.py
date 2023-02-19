from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
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


@router.get('/search', response_model=List[profile.ProfileResponseSchema])
def search(text: Optional[str] = '', min_followers: Optional[int] = None, max_followers: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Profile)
    if text:
        query = query.filter(or_(Profile.username.ilike(
            f"%{text}%"), Profile.bio.ilike(f"%{text}%")))
    if min_followers:
        query = query.filter(Profile.followers >= min_followers)
    if max_followers:
        query = query.filter(Profile.followers <= max_followers)

    query = query.order_by(Profile.created_at.asc())
    return query.all()
