from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product
from typing import List, Dict, Optional
import random


class RecommendationEngine:
    def __init__(self):
        pass
    
    def get_recommendations(
        self, 
        db: Session, 
        user_id: int, 
        limit: int = 10,
        context: Optional[str] = "homepage"
    ) -> List[Dict]:
        user_orders = db.query(Order).filter(Order.user_id == user_id).all()
        
        purchased_product_ids = set()
        for order in user_orders:
            for item in order.items:
                purchased_product_ids.add(item.product_id)
        
        all_products = db.query(Product).filter(Product.stock > 0).all()
        
        if not user_orders:
            recommended = random.sample(all_products, min(limit, len(all_products)))
            return [
                {"product_id": p.id, "score": 0.5 + random.random() * 0.5}
                for p in recommended
            ]
        
        category_counts = {}
        for order in user_orders:
            for item in order.items:
                product = db.query(Product).filter(Product.id == item.product_id).first()
                if product:
                    category_counts[product.category] = category_counts.get(product.category, 0) + 1
        
        favorite_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        favorite_category_names = [cat for cat, _ in favorite_categories]
        
        candidates = []
        for product in all_products:
            if product.id not in purchased_product_ids:
                score = 0.3
                if product.category in favorite_category_names:
                    score += 0.5
                score += random.random() * 0.2
                candidates.append({"product_id": product.id, "score": score})
        
        candidates.sort(key=lambda x: x["score"], reverse=True)
        
        return candidates[:limit]


recommender = RecommendationEngine()
