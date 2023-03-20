from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.cors.database import get_db
from app.cors.security import get_current_user
from app.api.schema import profile
from app.db.models.users import Profile, User

router = APIRouter()


def existing_user_profile(db: Session, auth_user: User):
    return (
        db.query(Profile).filter(Profile.owner_id == auth_user.id).first() is not None
    )


@router.post("/profile", response_model=profile.ProfileResponseSchema, status_code=201)
def create_profile(
    data_in: profile.ProfileCreate,
    db: Session = Depends(get_db),
    auth_user: User = Depends(get_current_user),
):
    existing_profile = existing_user_profile(db, auth_user)
    if existing_profile:
        raise HTTPException(
            status_code=403, detail=f"Users cannot have more than one profile"
        )
    profile = Profile(owner_id=auth_user.id, **data_in.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile
