# Sanset FastAPI Backend

**AI-powered e-commerce platform with ML-based recommendations, cart management, and order processing**

---

## ⚡ Quick Start Commands

### Install & Run (One Command)
```bash
# Server is already running! Just add sample data:
python seed_data.py
```

### Manual Install & Run
```bash
# 1. Install dependencies (already done in Replit)
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings python-jose passlib bcrypt python-multipart email-validator scikit-learn pandas numpy python-dateutil apscheduler

# 2. Start the server
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload

# 3. Add sample data (in a new terminal)
python seed_data.py
```

### View All Endpoints in One Place
```bash
# Open in browser:
http://localhost:5000/api-endpoints

# Or use curl:
curl http://localhost:5000/api-endpoints
```

### Interactive API Documentation
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc
- **All Endpoints**: http://localhost:5000/api-endpoints

### Test Credentials (after running seed_data.py)
```
Admin: admin@sanset.com / admin123456
User:  om@example.com / password123
```

---

## 🚀 Features

- **Authentication**: JWT-based auth with access & refresh tokens
- **User Management**: Profile, preferences, and address management
- **Product Catalog**: Full product CRUD with search and filtering
- **Smart Search**: Fuzzy search with typeahead suggestions
- **Shopping Cart**: Add/remove items, persistent cart storage
- **Order Processing**: Checkout with stock reservation and ETA calculation
- **ML Recommendations**: Personalized product recommendations based on user behavior
- **NoSQL Support**: PostgreSQL with JSONB for flexible document storage
- **Auto Documentation**: Interactive API docs at `/docs` (Swagger) and `/redoc`

## 📁 Project Structure

```
sanset-backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── config.py           # Settings and configuration
│   │   └── security.py         # JWT & password hashing
│   ├── api/
│   │   ├── deps.py             # Common dependencies
│   │   └── v1/
│   │       ├── auth.py         # Register, login, refresh
│   │       ├── users.py        # User profile endpoints
│   │       ├── products.py     # Product management
│   │       ├── cart.py         # Shopping cart
│   │       ├── orders.py       # Checkout & orders
│   │       ├── recommend.py    # ML recommendations
│   │       └── search.py       # Search & suggestions
│   ├── crud/                   # Database operations
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── db/
│   │   └── session.py          # Database connection
│   └── ml/
│       └── recommender.py      # Recommendation engine
├── seed_data.py                # Database seeding script
├── README.md                   # This file
└── pyproject.toml              # Dependencies
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.121+
- **Database**: PostgreSQL (with SQLite support for dev)
- **ORM**: SQLAlchemy 2.0
- **Auth**: JWT (python-jose) + bcrypt
- **ML**: Scikit-learn, NumPy, Pandas
- **Validation**: Pydantic 2.0

## ⚡ Quick Start

### 1. Install Dependencies

Dependencies are already installed in the Replit environment.

### 2. Start the Server

The server is already running on port 5000. You can restart it with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

### 3. Seed Sample Data

```bash
python seed_data.py
```

This creates:
- Admin user: `admin@sanset.com` / `admin123456`
- Sample user: `om@example.com` / `password123`
- 10 sample products across various categories

### 4. Explore the API

- **API Docs**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc
- **Health Check**: http://localhost:5000/healthz

## 📡 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Create new user
- `POST /api/v1/auth/login` - Login and get tokens
- `POST /api/v1/auth/refresh` - Refresh access token

### Users

- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update profile/preferences

### Products

- `GET /api/v1/products` - List products (with pagination, search, category filter)
- `GET /api/v1/products/{id}` - Get product details
- `POST /api/v1/products` - Create product (admin only)
- `PUT /api/v1/products/{id}` - Update product (admin only)

### Search

- `GET /api/v1/search?q=bread` - Search products
- `GET /api/v1/search/suggestions?q=bre` - Get search suggestions

### Cart

- `GET /api/v1/cart` - Get cart contents
- `POST /api/v1/cart/add` - Add item to cart
- `POST /api/v1/cart/remove` - Remove item from cart

### Orders

- `POST /api/v1/orders/checkout` - Create order from cart
- `GET /api/v1/orders/{id}` - Get order details
- `GET /api/v1/orders` - List user's orders
- `POST /api/v1/orders/addresses` - Create delivery address
- `GET /api/v1/orders/addresses` - List addresses

### Recommendations

- `GET /api/v1/recommend/{user_id}` - Get recommendations for user
- `GET /api/v1/recommend/me` - Get recommendations for current user

## 🧪 Example Usage

### Register & Login

```bash
# Register
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone": "+919999999999",
    "password": "securepass123"
  }'

# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### Browse Products

```bash
# List all products
curl http://localhost:5000/api/v1/products

# Search products
curl "http://localhost:5000/api/v1/search?q=bread&category=Bakery"

# Get product details
curl http://localhost:5000/api/v1/products/1
```

### Shopping Flow

```bash
# Add to cart (requires auth token)
curl -X POST http://localhost:5000/api/v1/cart/add \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "qty": 2}'

# View cart
curl http://localhost:5000/api/v1/cart \
  -H "Authorization: Bearer YOUR_TOKEN"

# Checkout
curl -X POST http://localhost:5000/api/v1/orders/checkout \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_method": "UPI",
    "address_id": 1,
    "coupon_code": "SAVE20"
  }'
```

### Get Recommendations

```bash
curl http://localhost:5000/api/v1/recommend/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🗄️ Database Models

### Core Tables

- **users**: User accounts with preferences (JSONB)
- **products**: Product catalog with flexible attributes (JSONB)
- **orders**: Order records with metadata (JSONB)
- **order_items**: Line items in orders
- **carts**: User shopping carts
- **cart_items**: Items in carts
- **addresses**: Delivery addresses
- **recommendations_log**: Recommendation history

### NoSQL Features (PostgreSQL JSONB)

The backend uses PostgreSQL's JSONB columns for flexible data:

- `users.preferences` - User settings, diet preferences, etc.
- `products.attributes` - Variable product attributes
- `orders.order_metadata` - Order metadata and tracking info

Example:
```python
# Product with flexible attributes
{
  "name": "Organic Bananas",
  "attributes": {
    "weight": "1kg",
    "organic": true,
    "origin": "India"
  }
}

# User with preferences
{
  "email": "om@example.com",
  "preferences": {
    "diet": "vegan",
    "delivery_speed": "express",
    "notifications": true
  }
}
```

## 🤖 ML Recommendation Engine

The recommendation system uses:

1. **Collaborative filtering**: Based on user purchase history
2. **Category affinity**: Recommends from favorite categories
3. **Content-based**: Product similarity
4. **Cold start handling**: Random popular products for new users

Algorithm:
```python
def get_recommendations(user_id, context):
    # 1. Analyze user's past orders
    # 2. Find favorite categories
    # 3. Score products based on:
    #    - Category match (0.5 weight)
    #    - Base popularity (0.3)
    #    - Random exploration (0.2)
    # 4. Return top-K scored products
```

## 🔒 Security

- **Password Hashing**: bcrypt
- **JWT Tokens**: 
  - Access token: 60 minutes
  - Refresh token: 30 days
- **CORS**: Configured for cross-origin requests
- **Input Validation**: Pydantic schemas
- **SQL Injection Protection**: SQLAlchemy ORM

## 🚀 Deployment

The app is configured for Replit deployment with:
- Port 5000 binding
- Environment variable support
- SQLite for dev (easily switch to PostgreSQL)

## 📊 API Response Examples

### Product List
```json
{
  "total": 10,
  "page": 1,
  "size": 20,
  "items": [
    {
      "id": 1,
      "name": "Whole Wheat Bread",
      "slug": "whole-wheat-bread",
      "category": "Bakery",
      "price": 40.0,
      "stock": 50,
      "attributes": {"weight": "500g", "organic": true}
    }
  ]
}
```

### Cart
```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "name": "Whole Wheat Bread",
      "qty": 2,
      "price": 40.0
    }
  ],
  "total": 80.0
}
```

### Recommendations
```json
{
  "user_id": 1,
  "recommendations": [
    {"product_id": 3, "score": 0.94},
    {"product_id": 7, "score": 0.82}
  ]
}
```

## 🛠️ Development

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-min-32-chars
DATABASE_URL=sqlite:///./sanset.db
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_MINUTES=43200
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests (when implemented)
pytest
```

## 📝 License

This project is open source and available under the MIT License.

## 👥 Credits

Built with ❤️ using FastAPI, SQLAlchemy, and modern Python best practices.
