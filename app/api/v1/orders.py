from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.order import CheckoutRequest, CheckoutResponse, OrderOut, AddressCreate, AddressOut
from app.crud import order as crud_order
from app.api.deps import get_current_active_user
from app.models.user import User
from app.models.address import Address

router = APIRouter()


@router.post("/checkout", response_model=CheckoutResponse)
def checkout(
    checkout_data: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    order = crud_order.create_order_from_cart(
        db,
        user_id=current_user.id,
        payment_method=checkout_data.payment_method,
        address_id=checkout_data.address_id,
        coupon_code=checkout_data.coupon_code
    )
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty or products unavailable"
        )
    
    return {
        "order_id": order.id,
        "status": order.status,
        "total_amount": order.total_amount,
        "payment_url": f"https://payment.gateway/pay/{order.id}",
        "placed_at": order.placed_at,
        "delivery_eta": order.delivery_eta
    }


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    order = crud_order.get_order_by_id(db, order_id=order_id, user_id=current_user.id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.get("", response_model=list[OrderOut])
def get_user_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return crud_order.get_user_orders(db, user_id=current_user.id)


@router.post("/addresses", response_model=AddressOut, status_code=status.HTTP_201_CREATED)
def create_address(
    address: AddressCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_address = Address(user_id=current_user.id, **address.model_dump())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


@router.get("/addresses", response_model=list[AddressOut])
def get_addresses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return db.query(Address).filter(Address.user_id == current_user.id).all()
