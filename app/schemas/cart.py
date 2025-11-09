from pydantic import BaseModel
from typing import List


class CartItemBase(BaseModel):
    product_id: int
    qty: int


class CartItemOut(BaseModel):
    product_id: int
    qty: int
    price: float
    name: str
    
    class Config:
        from_attributes = True


class CartOut(BaseModel):
    user_id: int
    items: List[CartItemOut]
    total: float


class AddToCart(BaseModel):
    product_id: int
    qty: int = 1


class RemoveFromCart(BaseModel):
    product_id: int
