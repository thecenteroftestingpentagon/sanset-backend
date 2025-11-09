from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    price: float
    stock: int
    image_url: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = {}


class ProductCreate(ProductBase):
    slug: str


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None


class ProductOut(ProductBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductList(BaseModel):
    total: int
    page: int
    size: int
    items: list[ProductOut]
