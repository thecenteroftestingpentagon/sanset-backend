from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class OrderItemOut(BaseModel):
    product_id: int
    qty: int
    price_at_purchase: float
    
    class Config:
        from_attributes = True


class CheckoutRequest(BaseModel):
    payment_method: str
    address_id: int
    coupon_code: Optional[str] = None


class OrderOut(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    payment_method: Optional[str]
    payment_status: str
    placed_at: datetime
    delivery_eta: Optional[datetime]
    items: List[OrderItemOut]
    
    class Config:
        from_attributes = True


class CheckoutResponse(BaseModel):
    order_id: int
    status: str
    total_amount: float
    payment_url: Optional[str]
    placed_at: datetime
    delivery_eta: Optional[datetime]


class AddressCreate(BaseModel):
    label: str
    address_line: str
    city: str
    state: Optional[str] = None
    pincode: str
    lat: Optional[float] = None
    lng: Optional[float] = None


class AddressOut(BaseModel):
    id: int
    user_id: int
    label: str
    address_line: str
    city: str
    state: Optional[str]
    pincode: str
    lat: Optional[float]
    lng: Optional[float]
    
    class Config:
        from_attributes = True
