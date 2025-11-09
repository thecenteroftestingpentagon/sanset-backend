from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.recommendation import RecommendationResponse
from app.ml.recommender import recommender
from app.api.deps import get_current_active_user
from app.models.user import User
from app.crud import user as crud_user
from typing import Optional

router = APIRouter()


@router.get("/{user_id}", response_model=RecommendationResponse)
def get_recommendations(
    user_id: int,
    context: Optional[str] = Query("homepage"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    user = crud_user.get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    recommendations = recommender.get_recommendations(db, user_id=user_id, limit=limit, context=context)
    
    return {
        "user_id": user_id,
        "recommendations": recommendations
    }


@router.get("/me", response_model=RecommendationResponse)
def get_my_recommendations(
    context: Optional[str] = Query("homepage"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    recommendations = recommender.get_recommendations(
        db, user_id=current_user.id, limit=limit, context=context
    )
    
    return {
        "user_id": current_user.id,
        "recommendations": recommendations
    }
