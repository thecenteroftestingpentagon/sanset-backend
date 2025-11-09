from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.cart import Cart, CartItem
from datetime import datetime, timedelta
from typing import Optional, List


def create_order_from_cart(
    db: Session, 
    user_id: int, 
    payment_method: str,
    address_id: int,
    coupon_code: Optional[str] = None
) -> Optional[Order]:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart or not cart.items:
        return None
    
    total_amount = 0.0
    order_items_data = []
    
    for cart_item in cart.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()
        if not product or product.stock < cart_item.qty:
            continue
        
        item_total = product.price * cart_item.qty
        total_amount += item_total
        
        order_items_data.append({
            "product": product,
            "product_id": product.id,
            "qty": cart_item.qty,
            "price": product.price
        })
    
    if not order_items_data:
        return None
    
    try:
        for item_data in order_items_data:
            item_data["product"].stock -= item_data["qty"]
        
        delivery_eta = datetime.utcnow() + timedelta(minutes=30)
        
        order = Order(
            user_id=user_id,
            total_amount=total_amount,
            payment_method=payment_method,
            address_id=address_id,
            coupon_code=coupon_code,
            delivery_eta=delivery_eta,
            status="placed",
            payment_status="pending"
        )
        
        db.add(order)
        db.flush()
        
        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data["product_id"],
                qty=item_data["qty"],
                price_at_purchase=item_data["price"]
            )
            db.add(order_item)
        
        for cart_item in cart.items:
            db.delete(cart_item)
        
        db.commit()
        db.refresh(order)
        
        return order
    
    except Exception as e:
        db.rollback()
        raise e


def get_order_by_id(db: Session, order_id: int, user_id: Optional[int] = None) -> Optional[Order]:
    query = db.query(Order).filter(Order.id == order_id)
    if user_id:
        query = query.filter(Order.user_id == user_id)
    return query.first()


def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 20) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()
