from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import ProductOut
from app.models.product import Product
from typing import List, Optional

router = APIRouter()


@router.get("", response_model=List[ProductOut])
def search_products(
    q: str = Query(..., min_length=1),
    category: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if category:
        query = query.filter(Product.category == category)
    
    query = query.filter(
        (Product.name.ilike(f"%{q}%")) | 
        (Product.description.ilike(f"%{q}%"))
    )
    
    products = query.limit(limit).all()
    return products


@router.get("/suggestions", response_model=List[str])
def get_suggestions(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    products = db.query(Product.name).filter(
        Product.name.ilike(f"%{q}%")
    ).limit(10).all()
    
    return [p.name for p in products]
