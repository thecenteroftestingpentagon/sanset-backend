from pydantic import BaseModel
from typing import List


class RecommendationItem(BaseModel):
    product_id: int
    score: float


class RecommendationResponse(BaseModel):
    user_id: int
    recommendations: List[RecommendationItem]
