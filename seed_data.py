#!/usr/bin/env python3
"""
Seed script to populate the Sanset database with sample data.
Run this after starting the server: python seed_data.py
"""

import requests
import json

BASE_URL = "http://localhost:5000/api/v1"

def create_admin_user():
    """Create an admin user"""
    user_data = {
        "full_name": "Admin User",
        "email": "admin@sanset.com",
        "phone": "+919876543210",
        "password": "admin123456"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code == 201:
        print(f"✓ Created admin user: {user_data['email']}")
        
        login_response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        
        if login_response.status_code == 200:
            return login_response.json()["access_token"]
    else:
        print(f"✗ Admin user might already exist or error: {response.text}")
        
        login_response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        if login_response.status_code == 200:
            return login_response.json()["access_token"]
    
    return None


def create_sample_user():
    """Create a sample regular user"""
    user_data = {
        "full_name": "Om Choksi",
        "email": "om@example.com",
        "phone": "+919999999999",
        "password": "password123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
    if response.status_code == 201:
        print(f"✓ Created sample user: {user_data['email']}")
    else:
        print(f"✗ Sample user might already exist: {response.text}")


def create_products(token):
    """Create sample products"""
    products = [
        {
            "name": "Whole Wheat Bread",
            "slug": "whole-wheat-bread",
            "category": "Bakery",
            "description": "Fresh baked whole wheat bread, healthy and delicious",
            "price": 40.0,
            "stock": 50,
            "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff",
            "attributes": {"weight": "500g", "organic": True}
        },
        {
            "name": "Fresh Milk",
            "slug": "fresh-milk",
            "category": "Dairy",
            "description": "Farm fresh pasteurized milk",
            "price": 60.0,
            "stock": 100,
            "image_url": "https://images.unsplash.com/photo-1550583724-b2692b85b150",
            "attributes": {"volume": "1L", "fat_content": "3.5%"}
        },
        {
            "name": "Organic Bananas",
            "slug": "organic-bananas",
            "category": "Fruits",
            "description": "Fresh organic bananas, rich in potassium",
            "price": 50.0,
            "stock": 75,
            "image_url": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e",
            "attributes": {"weight": "1kg", "organic": True}
        },
        {
            "name": "Basmati Rice",
            "slug": "basmati-rice",
            "category": "Grains",
            "description": "Premium quality aged basmati rice",
            "price": 150.0,
            "stock": 200,
            "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c",
            "attributes": {"weight": "5kg", "aged": "2 years"}
        },
        {
            "name": "Fresh Tomatoes",
            "slug": "fresh-tomatoes",
            "category": "Vegetables",
            "description": "Fresh red tomatoes, perfect for cooking",
            "price": 30.0,
            "stock": 60,
            "image_url": "https://images.unsplash.com/photo-1546094096-0df4bcaaa337",
            "attributes": {"weight": "500g"}
        },
        {
            "name": "Greek Yogurt",
            "slug": "greek-yogurt",
            "category": "Dairy",
            "description": "Thick and creamy Greek yogurt",
            "price": 80.0,
            "stock": 40,
            "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777",
            "attributes": {"volume": "500g", "protein": "high"}
        },
        {
            "name": "Chocolate Chip Cookies",
            "slug": "chocolate-chip-cookies",
            "category": "Bakery",
            "description": "Homemade style chocolate chip cookies",
            "price": 120.0,
            "stock": 30,
            "image_url": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e",
            "attributes": {"count": "12 pieces"}
        },
        {
            "name": "Fresh Orange Juice",
            "slug": "fresh-orange-juice",
            "category": "Beverages",
            "description": "100% fresh squeezed orange juice",
            "price": 90.0,
            "stock": 25,
            "image_url": "https://images.unsplash.com/photo-1600271886742-f049cd451bba",
            "attributes": {"volume": "1L", "preservatives": False}
        },
        {
            "name": "Almonds",
            "slug": "almonds",
            "category": "Dry Fruits",
            "description": "Premium quality California almonds",
            "price": 450.0,
            "stock": 50,
            "image_url": "https://images.unsplash.com/photo-1508747703725-719777637510",
            "attributes": {"weight": "500g", "type": "California"}
        },
        {
            "name": "Green Tea",
            "slug": "green-tea",
            "category": "Beverages",
            "description": "Organic green tea leaves",
            "price": 200.0,
            "stock": 35,
            "image_url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc",
            "attributes": {"count": "50 bags", "organic": True}
        }
    ]
    
    headers = {"Authorization": f"Bearer {token}"}
    created_count = 0
    
    for product in products:
        response = requests.post(f"{BASE_URL}/products", json=product, headers=headers)
        if response.status_code == 201:
            created_count += 1
            print(f"✓ Created product: {product['name']}")
        else:
            print(f"✗ Failed to create {product['name']}: {response.text}")
    
    print(f"\n✓ Created {created_count} products total")


def main():
    print("=" * 60)
    print("Sanset Database Seeding Script")
    print("=" * 60)
    print()
    
    print("Creating admin user...")
    token = create_admin_user()
    
    if not token:
        print("\n✗ Failed to get admin token. Please check if the server is running.")
        return
    
    print("\nCreating sample user...")
    create_sample_user()
    
    print("\nCreating sample products...")
    create_products(token)
    
    print("\n" + "=" * 60)
    print("✓ Database seeding completed!")
    print("=" * 60)
    print("\nYou can now:")
    print("  1. Visit http://localhost:5000/docs for API documentation")
    print("  2. Login with: admin@sanset.com / admin123456")
    print("  3. Or login with: om@example.com / password123")
    print()


if __name__ == "__main__":
    main()
