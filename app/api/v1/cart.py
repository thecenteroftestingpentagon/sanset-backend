from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.cart import CartOut, AddToCart, RemoveFromCart
from app.crud import cart as crud_cart
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("", response_model=CartOut)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return crud_cart.get_cart_with_items(db, user_id=current_user.id)


@router.post("/add", response_model=CartOut)
def add_to_cart(
    item: AddToCart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    crud_cart.add_to_cart(db, user_id=current_user.id, product_id=item.product_id, qty=item.qty)
    return crud_cart.get_cart_with_items(db, user_id=current_user.id)


@router.post("/remove", response_model=CartOut)
def remove_from_cart(
    item: RemoveFromCart,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    crud_cart.remove_from_cart(db, user_id=current_user.id, product_id=item.product_id)
    return crud_cart.get_cart_with_items(db, user_id=current_user.id)
