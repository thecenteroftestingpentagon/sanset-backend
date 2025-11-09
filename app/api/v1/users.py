from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserOut, UserUpdate
from app.crud import user as crud_user
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserOut)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/me", response_model=UserOut)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    updated_user = crud_user.update_user(db, user_id=current_user.id, user_update=user_update)
    return updated_user
