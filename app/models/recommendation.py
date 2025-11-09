from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from datetime import datetime
from app.db.session import Base


class RecommendationLog(Base):
    __tablename__ = "recommendations_log"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recommended_products = Column(JSON, nullable=False)
    context = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow)
