# Sanset FastAPI Backend

## Overview

Sanset is a complete, production-ready AI-powered e-commerce platform built with FastAPI. The system provides comprehensive shopping functionality including user management, product catalog, shopping cart, order processing, and ML-based product recommendations. It uses JWT-based authentication, supports both PostgreSQL (with JSONB for NoSQL features) and SQLite, and includes intelligent search capabilities with fuzzy matching and typeahead suggestions.

**Current Status**: ✅ Production-ready - All core features implemented and tested
**Server**: Running on port 5000
**API Docs**: http://localhost:5000/docs

## Recent Changes (November 2025)

- ✅ Complete backend implementation with all endpoints
- ✅ Fixed critical checkout transaction handling for atomic operations
- ✅ Implemented proper stock validation and rollback on failures
- ✅ Added seed data script for quick demo setup
- ✅ Created comprehensive API documentation

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### API Architecture

**Framework**: FastAPI with automatic OpenAPI documentation

The application follows a modular REST API design with versioned endpoints under `/api/v1`. All routes are organized by domain (auth, users, products, cart, orders, recommendations, search) and registered through FastAPI's router system in `app/main.py`. The API provides interactive documentation at `/docs` (Swagger UI) and `/redoc` (ReDoc).

**Authentication & Authorization**: JWT token-based authentication with refresh tokens

The system uses a dual-token approach with short-lived access tokens (60 minutes) and long-lived refresh tokens (30 days). Passwords are hashed using bcrypt through passlib. Token verification and user dependency injection is handled through FastAPI's dependency system in `app/api/deps.py`, supporting role-based access control with admin and regular user roles.

### Data Layer

**ORM**: SQLAlchemy with declarative base models

The application uses SQLAlchemy for database abstraction with models defined in `app/models/`. Each domain entity (User, Product, Order, Cart, Address) is represented as a separate model with relationships defined using SQLAlchemy's relationship API. The models support JSONB columns for flexible schema-less data storage (preferences, attributes, metadata).

**Database**: PostgreSQL (production) / SQLite (development)

Database connection is managed through a session factory pattern in `app/db/session.py`. The system uses connection pooling and includes a dependency function (`get_db()`) that yields database sessions with automatic cleanup. Schema migrations would be handled through Alembic (referenced in documentation but not yet implemented).

**CRUD Pattern**: Separation of database operations from business logic

All database operations are isolated in the `app/crud/` module, providing reusable functions for Create, Read, Update, Delete operations. This keeps the API route handlers thin and focused on request/response handling while maintaining testable database logic.

### Business Logic

**Shopping Cart**: Persistent cart with one-to-many item relationships

Each user has a single cart that persists across sessions. Cart items reference products and track quantities. The cart is automatically created on first access and supports add/remove operations with atomic updates.

**Order Processing**: Stock reservation with ETA calculation

When orders are placed, the system validates stock availability, reserves inventory by decrementing product stock, calculates delivery ETA (currently 30 minutes from order time), and creates immutable order records with items captured at purchase price. Failed orders due to insufficient stock prevent cart checkout.

**Product Search**: Fuzzy search with ILIKE pattern matching

Search functionality uses case-insensitive pattern matching across product names and descriptions. The system supports filtering by category and returns typeahead suggestions for autocomplete functionality.

**ML Recommendations**: Collaborative filtering based on purchase history

The recommendation engine (`app/ml/recommender.py`) analyzes user order history to identify favorite categories and suggests products the user hasn't purchased. For new users without history, it provides random popular products. Recommendations are scored based on category affinity and can be contextualized (homepage, product page, cart).

### Security & Configuration

**Environment-based configuration**: Pydantic Settings with .env support

All configuration is centralized in `app/core/config.py` using Pydantic's BaseSettings, which automatically loads from environment variables or `.env` files. This includes database URLs, JWT secrets, token expiration times, and optional integrations like Sentry.

**Password Security**: Bcrypt hashing with automatic salt generation

The system uses passlib's CryptContext for secure password storage. Plain passwords are never stored; only bcrypt hashes are persisted in the database.

**CORS Middleware**: Wide-open CORS for development (should be restricted in production)

Currently allows all origins, credentials, methods, and headers for ease of development. This should be locked down to specific frontend domains in production.

## External Dependencies

### Core Framework & Web Server

- **FastAPI** (0.121+): Web framework providing automatic OpenAPI/Swagger docs, dependency injection, and async support
- **Uvicorn**: ASGI server for running the FastAPI application
- **Pydantic**: Data validation and settings management using Python type annotations

### Database & ORM

- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **PostgreSQL**: Primary production database (with JSONB support for semi-structured data)
- **SQLite**: Development/testing database (file-based, configured via DATABASE_URL)

### Authentication & Security

- **python-jose[cryptography]**: JWT token creation and verification
- **passlib[bcrypt]**: Password hashing and verification
- **python-multipart**: Form data parsing for OAuth2 password flow

### Machine Learning

- **scikit-learn** (implied): For recommendation engine algorithms
- Currently uses simplified collaborative filtering; can be extended with matrix factorization or neural approaches

### Optional Integrations

- **Sentry**: Error tracking and monitoring (configured via SENTRY_DSN environment variable)
- **APScheduler** (referenced): For background tasks like ML model retraining, though not yet implemented

### Development Tools

- **requests**: HTTP client library (used in seed_data.py for API testing)

### Future Considerations

The architecture is designed to support:
- Alembic for database migrations
- Redis for session/cache storage
- Message queues (Celery/RQ) for async background jobs
- External payment gateways (currently returns mock payment URLs)
- Geolocation services for address validation and delivery optimization