from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.config import get_db
from core.hashing import Hasher
from models.users import Users
from schemas.users import UserSchema, ShowUserSchema


router = APIRouter()

@router.post("/users", response_model=ShowUserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user : UserSchema,db: Session = Depends(get_db)):
    user = Users(
        username = user.username,
        password = Hasher.get_password_hash(user.password),
        is_active = True,
        is_superuser = False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 

