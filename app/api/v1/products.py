from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate, ProductList
from app.crud import product as crud_product
from app.api.deps import get_current_admin
from typing import Optional

router = APIRouter()


@router.get("", response_model=ProductList)
def list_products(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    q: Optional[str] = None,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * size
    products, total = crud_product.get_products(
        db, skip=skip, limit=size, category=category, search=q
    )
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": products
    }


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get_product_by_id(db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    existing_product = crud_product.get_product_by_slug(db, slug=product.slug)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this slug already exists"
        )
    
    return crud_product.create_product(db=db, product=product)


@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin)
):
    updated_product = crud_product.update_product(db, product_id=product_id, product_update=product_update)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated_product
