from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine, Base
from app.api.v1 import auth, users, products, cart, orders, recommend, search

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(products.router, prefix=f"{settings.API_V1_STR}/products", tags=["products"])
app.include_router(cart.router, prefix=f"{settings.API_V1_STR}/cart", tags=["cart"])
app.include_router(orders.router, prefix=f"{settings.API_V1_STR}/orders", tags=["orders"])
app.include_router(recommend.router, prefix=f"{settings.API_V1_STR}/recommend", tags=["recommend"])
app.include_router(search.router, prefix=f"{settings.API_V1_STR}/search", tags=["search"])


@app.get("/")
def root():
    return {
        "message": "Sanset FastAPI Backend",
        "version": settings.VERSION,
        "docs": "/docs",
        "api": settings.API_V1_STR
    }


@app.get("/healthz")
def health_check():
    return {"status": "healthy"}


@app.get("/api-endpoints")
def list_all_endpoints():
    """
    📚 Complete API Documentation - All Endpoints in One Place
    """
    return {
        "project": "Sanset E-Commerce API",
        "base_url": settings.API_V1_STR,
        "authentication": {
            "description": "JWT-based authentication with access and refresh tokens",
            "endpoints": {
                "POST /api/v1/auth/register": {
                    "description": "Register a new user",
                    "body": {
                        "full_name": "string",
                        "email": "string",
                        "phone": "string",
                        "password": "string (min 8 chars)"
                    },
                    "response": "User object with tokens"
                },
                "POST /api/v1/auth/login": {
                    "description": "Login with email and password",
                    "body": {
                        "email": "string",
                        "password": "string"
                    },
                    "response": "Access token (60 min) and refresh token (30 days)"
                },
                "POST /api/v1/auth/refresh": {
                    "description": "Get new access token using refresh token",
                    "body": {
                        "refresh_token": "string"
                    },
                    "response": "New access token"
                }
            }
        },
        "users": {
            "description": "User profile and address management",
            "auth_required": "Yes (Bearer token)",
            "endpoints": {
                "GET /api/v1/users/me": {
                    "description": "Get current user profile",
                    "response": "User object with preferences (JSONB)"
                },
                "PUT /api/v1/users/me": {
                    "description": "Update user profile",
                    "body": {
                        "full_name": "string (optional)",
                        "phone": "string (optional)",
                        "preferences": "object (optional, stored in JSONB)"
                    }
                },
                "GET /api/v1/users/me/addresses": {
                    "description": "List user's saved addresses"
                },
                "POST /api/v1/users/me/addresses": {
                    "description": "Add new delivery address",
                    "body": {
                        "address_line1": "string",
                        "address_line2": "string (optional)",
                        "city": "string",
                        "state": "string",
                        "pincode": "string",
                        "is_default": "boolean (optional)"
                    }
                },
                "GET /api/v1/users/": {
                    "description": "List all users (Admin only)",
                    "auth": "Admin role required"
                }
            }
        },
        "products": {
            "description": "Product catalog with flexible JSONB attributes",
            "endpoints": {
                "GET /api/v1/products/": {
                    "description": "List all products with pagination",
                    "query_params": {
                        "skip": "int (default 0)",
                        "limit": "int (default 100)",
                        "category": "string (optional filter)"
                    }
                },
                "GET /api/v1/products/{id}": {
                    "description": "Get product details by ID",
                    "response": "Product with attributes stored in JSONB (weight, organic, etc.)"
                },
                "POST /api/v1/products/": {
                    "description": "Create new product (Admin only)",
                    "auth": "Admin role required",
                    "body": {
                        "name": "string",
                        "description": "string",
                        "price": "float",
                        "category": "string",
                        "stock": "int",
                        "image_url": "string (optional)",
                        "attributes": "object (JSONB - flexible fields)"
                    }
                },
                "PUT /api/v1/products/{id}": {
                    "description": "Update product (Admin only)",
                    "auth": "Admin role required"
                },
                "DELETE /api/v1/products/{id}": {
                    "description": "Delete product (Admin only)",
                    "auth": "Admin role required"
                }
            }
        },
        "search": {
            "description": "Intelligent product search with fuzzy matching",
            "endpoints": {
                "GET /api/v1/search/": {
                    "description": "Search products by name/description",
                    "query_params": {
                        "q": "string (search query)",
                        "category": "string (optional filter)",
                        "limit": "int (default 20)"
                    }
                },
                "GET /api/v1/search/typeahead": {
                    "description": "Get autocomplete suggestions",
                    "query_params": {
                        "q": "string (partial text)",
                        "limit": "int (default 10)"
                    }
                }
            }
        },
        "cart": {
            "description": "Shopping cart management (persistent across sessions)",
            "auth_required": "Yes (Bearer token)",
            "endpoints": {
                "GET /api/v1/cart/": {
                    "description": "Get current user's cart with all items"
                },
                "POST /api/v1/cart/items": {
                    "description": "Add item to cart",
                    "body": {
                        "product_id": "int",
                        "qty": "int (default 1)"
                    }
                },
                "DELETE /api/v1/cart/items/{product_id}": {
                    "description": "Remove item from cart"
                },
                "DELETE /api/v1/cart/": {
                    "description": "Clear entire cart"
                }
            }
        },
        "orders": {
            "description": "Order processing with atomic stock management",
            "auth_required": "Yes (Bearer token)",
            "endpoints": {
                "POST /api/v1/orders/checkout": {
                    "description": "Create order from cart (validates stock, atomic transaction)",
                    "body": {
                        "payment_method": "string (card/upi/cod)",
                        "address_id": "int",
                        "coupon_code": "string (optional)"
                    },
                    "response": "Order object with payment URL and ETA"
                },
                "GET /api/v1/orders/": {
                    "description": "List user's order history",
                    "query_params": {
                        "skip": "int (default 0)",
                        "limit": "int (default 100)"
                    }
                },
                "GET /api/v1/orders/{id}": {
                    "description": "Get order details by ID"
                },
                "GET /api/v1/orders/all": {
                    "description": "List all orders (Admin only)",
                    "auth": "Admin role required"
                }
            }
        },
        "recommendations": {
            "description": "ML-powered product recommendations",
            "auth_required": "Yes (Bearer token)",
            "endpoints": {
                "GET /api/v1/recommend/": {
                    "description": "Get personalized recommendations based on purchase history",
                    "query_params": {
                        "context": "string (homepage/product/cart)",
                        "limit": "int (default 10)"
                    },
                    "notes": "Uses collaborative filtering and category affinity"
                },
                "POST /api/v1/recommend/retrain": {
                    "description": "Retrain ML model (Admin only)",
                    "auth": "Admin role required"
                }
            }
        },
        "sample_credentials": {
            "admin": {
                "email": "admin@sanset.com",
                "password": "admin123456"
            },
            "user": {
                "email": "om@example.com",
                "password": "password123"
            },
            "note": "Run seed_data.py to create these users and sample products"
        },
        "interactive_docs": {
            "swagger_ui": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
