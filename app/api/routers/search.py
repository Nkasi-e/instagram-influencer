from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.cors.database import get_db
from app.api.schema import profile
from app.db.models.users import Profile


router = APIRouter()


@router.get('/search', response_model=List[profile.ProfileResponseSchema], status_code=200)
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
