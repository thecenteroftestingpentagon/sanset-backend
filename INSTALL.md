# Sanset Backend - Installation & Run Guide

## 🚀 Quick Start (Replit - Already Setup!)

Your server is already running! Just add sample data:

```bash
python seed_data.py
```

Then visit: **http://localhost:5000/api-endpoints**

---

## 📦 Manual Installation (Fresh Setup)

### Step 1: Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings python-jose passlib bcrypt python-multipart email-validator scikit-learn pandas numpy python-dateutil apscheduler
```

### Step 2: Start the Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

### Step 3: Add Sample Data

Open a new terminal and run:

```bash
python seed_data.py
```

---

## 📚 View All Endpoints

### Option 1: In Browser
Open: **http://localhost:5000/api-endpoints**

### Option 2: Command Line
```bash
curl http://localhost:5000/api-endpoints | jq
```

### Option 3: Interactive Docs
- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

---

## 🔑 Test Credentials

After running `seed_data.py`:

**Admin Account:**
- Email: `admin@sanset.com`
- Password: `admin123456`

**Regular User:**
- Email: `om@example.com`
- Password: `password123`

---

## 🧪 Quick Test

### 1. Register a New User
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "phone": "+919876543210",
    "password": "testpass123"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Copy the `access_token` from the response.

### 3. Get Your Profile
```bash
curl -X GET http://localhost:5000/api/v1/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 4. Browse Products
```bash
curl http://localhost:5000/api/v1/products/
```

### 5. Search Products
```bash
curl "http://localhost:5000/api/v1/search/?q=apple"
```

---

## 🗂️ All Available Endpoints

Visit **http://localhost:5000/api-endpoints** to see:

- ✅ Authentication (register, login, refresh)
- ✅ User Management (profile, addresses)
- ✅ Products (CRUD, search, filter)
- ✅ Shopping Cart (add, remove, view)
- ✅ Orders (checkout, history, tracking)
- ✅ ML Recommendations (personalized suggestions)
- ✅ Search (fuzzy search, typeahead)

---

## 🛠️ Development Commands

### Restart Server
```bash
pkill -f uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

### Reset Database
```bash
rm -f sanset.db
python seed_data.py
```

### Check Server Health
```bash
curl http://localhost:5000/healthz
```

---

## 🎯 Next Steps

1. **Explore the API**: Visit http://localhost:5000/api-endpoints
2. **Try Interactive Docs**: Visit http://localhost:5000/docs
3. **Test the Flow**: Register → Login → Browse → Add to Cart → Checkout
4. **Get Recommendations**: Use the `/api/v1/recommend/` endpoint
5. **Deploy**: Publish your app to get a live URL

---

## 💡 Tips

- All endpoints are documented at `/api-endpoints`
- Interactive testing available at `/docs`
- Sample data includes 10 products across categories
- JWT tokens expire in 60 minutes (refresh tokens last 30 days)
- PostgreSQL JSONB used for flexible product attributes & user preferences
