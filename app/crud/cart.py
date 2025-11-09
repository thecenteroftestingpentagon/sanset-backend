from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem
from app.models.product import Product
from typing import Optional


def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def add_to_cart(db: Session, user_id: int, product_id: int, qty: int) -> Cart:
    cart = get_or_create_cart(db, user_id)
    
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()
    
    if existing_item:
        existing_item.qty += qty
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, qty=qty)
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart)
    return cart


def remove_from_cart(db: Session, user_id: int, product_id: int) -> Cart:
    cart = get_or_create_cart(db, user_id)
    
    cart_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()
    
    if cart_item:
        db.delete(cart_item)
        db.commit()
        db.refresh(cart)
    
    return cart


def get_cart_with_items(db: Session, user_id: int):
    cart = get_or_create_cart(db, user_id)
    items = []
    total = 0.0
    
    for cart_item in cart.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if product:
            item_total = product.price * cart_item.qty
            items.append({
                "product_id": product.id,
                "name": product.name,
                "qty": cart_item.qty,
                "price": product.price
            })
            total += item_total
    
    return {"user_id": user_id, "items": items, "total": total}


def clear_cart(db: Session, user_id: int):
    cart = get_or_create_cart(db, user_id)
    for item in cart.items:
        db.delete(item)
    db.commit()
