# Items API — Full Documentation

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [File Breakdown](#4-file-breakdown)
5. [Database Design](#5-database-design)
6. [API Endpoints](#6-api-endpoints)
7. [Request & Response Schemas](#7-request--response-schemas)
8. [How to Run Locally](#8-how-to-run-locally)
9. [How to Test the API](#9-how-to-test-the-api)
10. [Deployment Guide (Render)](#10-deployment-guide-render)
11. [Android Integration Guide](#11-android-integration-guide)

---

## 1. Project Overview

**python-fastapi-demo** is a RESTful API for managing a list of items.
It supports creating, reading, and deleting items through standard HTTP endpoints.

Built as a backend demo to showcase:
- Clean Python API architecture
- Automatic API documentation via Swagger UI
- SQLite database with SQLAlchemy ORM
- Production-ready structure with easy PostgreSQL swap

---

## 2. Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.12 | Programming language |
| FastAPI | 0.115.6 | Web framework for building APIs |
| SQLAlchemy | 2.0.36 | ORM — talks to database using Python objects |
| Pydantic | 2.10.3 | Data validation and serialization |
| SQLite | Built-in | Local database (file-based, zero setup) |
| Uvicorn | 0.32.1 | ASGI server — runs the FastAPI app |

---

## 3. Project Structure

```
python-fastapi-demo/
│
├── main.py           → API entry point and route definitions
├── database.py       → Database connection and session management
├── models.py         → SQLAlchemy database table definition
├── schemas.py        → Pydantic request/response data models
├── requirements.txt  → Python package dependencies
├── .gitignore        → Files excluded from GitHub
├── README.md         → Quick start guide
├── DOCUMENTATION.md  → This file — full project documentation
│
├── items.db          → SQLite database file (auto-created on first run)
└── venv/             → Python virtual environment (not on GitHub)
```

---

## 4. File Breakdown

### `main.py`
The entry point of the application.

**Responsibilities:**
- Creates the FastAPI app instance with title, description, version
- Creates all database tables on startup (`Base.metadata.create_all`)
- Seeds 5 default items on first run if the database is empty
- Defines all 5 API route handlers

**Key dependencies imported:**
- `database.py` → `engine`, `get_db`, `Base`
- `models.py` → `Item`
- `schemas.py` → `ItemCreate`, `ItemResponse`

---

### `database.py`
Manages the database connection and session lifecycle.

**Responsibilities:**
- Defines the database URL (SQLite for local, PostgreSQL for production)
- Creates the SQLAlchemy engine (the actual database connection)
- Creates `SessionLocal` — a factory for database sessions
- Defines `Base` — the parent class all models inherit from
- Provides `get_db()` — a dependency that opens and closes DB sessions per request

**Switching to PostgreSQL:**
```python
# Replace this line in database.py:
DATABASE_URL = "sqlite:///./items.db"

# With this:
DATABASE_URL = "postgresql://user:password@host:5432/dbname"
```

---

### `models.py`
Defines the database table structure using SQLAlchemy.

**Responsibilities:**
- Defines the `Item` class which maps to the `items` table in the database
- Declares all columns with their types and constraints

**Table: `items`**
| Column | Type | Constraints |
|---|---|---|
| id | Integer | Primary key, auto-increment, indexed |
| name | String | Not null |
| description | String | Nullable (optional) |

---

### `schemas.py`
Defines the shape of data going in and out of the API using Pydantic.

**Responsibilities:**
- `ItemCreate` — validates incoming POST request body
- `ItemResponse` — shapes outgoing JSON responses
- Ensures wrong data types are rejected automatically

**Why two separate schemas:**
- `ItemCreate` has no `id` — client should not set the ID, the database does
- `ItemResponse` includes `id` — returned after DB assigns it
- `from_attributes = True` — allows Pydantic to read from SQLAlchemy model objects

---

### `requirements.txt`
Lists all Python packages needed to run the project.

```
fastapi==0.115.6
uvicorn==0.32.1
sqlalchemy==2.0.36
pydantic==2.10.3
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 5. Database Design

### Table: `items`

```
┌─────────────────────────────────────┐
│              items                  │
├──────┬────────────┬─────────────────┤
│  id  │    name    │   description   │
│ int  │   string   │     string?     │
│  PK  │  NOT NULL  │    NULLABLE     │
├──────┼────────────┼─────────────────┤
│  1   │ MacBook Pro│ Apple laptop    │
│  2   │ iPhone 16  │ Apple smartphone│
│  3   │ Samsung... │ Android phone   │
│  4   │ Sony WH... │ Headphones      │
│  5   │ iPad Pro   │ Apple tablet    │
└──────┴────────────┴─────────────────┘
```

These 5 rows are **seeded automatically** on the first run.

---

## 6. API Endpoints

### Base URL (local)
```
http://127.0.0.1:8000
```

---

### `GET /`
Health check — confirms the API is running.

**Response:**
```json
{ "message": "Items API is running!" }
```

---

### `GET /api/items`
Returns all items in the database.

**Response `200 OK`:**
```json
[
  { "id": 1, "name": "MacBook Pro", "description": "Apple laptop" },
  { "id": 2, "name": "iPhone 16", "description": "Apple smartphone" }
]
```

---

### `GET /api/items/{item_id}`
Returns a single item by its ID.

**Path parameter:** `item_id` (integer)

**Response `200 OK`:**
```json
{ "id": 1, "name": "MacBook Pro", "description": "Apple laptop" }
```

**Response `404 Not Found`:**
```json
{ "detail": "Item not found" }
```

---

### `POST /api/items`
Creates a new item.

**Request body:**
```json
{
  "name": "AirPods Pro",
  "description": "Wireless earbuds"
}
```
> `description` is optional. `name` is required.

**Response `201 Created`:**
```json
{ "id": 6, "name": "AirPods Pro", "description": "Wireless earbuds" }
```

---

### `DELETE /api/items/{item_id}`
Deletes an item by ID.

**Path parameter:** `item_id` (integer)

**Response `204 No Content`:** (empty body — success)

**Response `404 Not Found`:**
```json
{ "detail": "Item not found" }
```

---

## 7. Request & Response Schemas

### ItemCreate (Request)
```json
{
  "name": "string (required)",
  "description": "string or null (optional)"
}
```

### ItemResponse (Response)
```json
{
  "id": "integer",
  "name": "string",
  "description": "string or null"
}
```

---

## 8. How to Run Locally

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# Step 1 — Clone the repository
git clone https://github.com/ManojkumarKaliannan/python-fastapi-demo.git
cd python-fastapi-demo

# Step 2 — Create virtual environment
python3 -m venv venv

# Step 3 — Activate virtual environment
source venv/bin/activate          # Mac/Linux
venv\Scripts\activate             # Windows

# Step 4 — Install dependencies
pip install -r requirements.txt

# Step 5 — Start the server
uvicorn main:app --reload
```

Server will be live at: `http://127.0.0.1:8000`

To stop: press `Ctrl + C`

---

## 9. How to Test the API

### Option 1 — Swagger UI (Recommended)
Open in browser:
```
http://127.0.0.1:8000/docs
```
Click any endpoint → "Try it out" → "Execute" → see live response.

### Option 2 — ReDoc (Read-only docs)
```
http://127.0.0.1:8000/redoc
```

### Option 3 — Raw JSON in browser
```
http://127.0.0.1:8000/api/items
```

### Option 4 — curl (Terminal)
```bash
# Get all items
curl http://127.0.0.1:8000/api/items

# Get one item
curl http://127.0.0.1:8000/api/items/1

# Create item
curl -X POST http://127.0.0.1:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "AirPods Pro", "description": "Wireless earbuds"}'

# Delete item
curl -X DELETE http://127.0.0.1:8000/api/items/1
```

---

## 10. Deployment Guide (Render)

### Step 1 — Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/ManojkumarKaliannan/python-fastapi-demo.git
git push -u origin main
```

### Step 2 — Create Web Service on Render
1. Go to [render.com](https://render.com) → Sign up free
2. Click **New** → **Web Service**
3. Connect your GitHub account → Select `python-fastapi-demo`
4. Configure:

| Field | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Plan | Free |

5. Click **Create Web Service**

### Step 3 — Your API is live
```
https://python-fastapi-demo-xxxx.onrender.com/docs
```

> **Note:** Free tier sleeps after 15 mins of inactivity. First request after sleep takes ~30 seconds.

---

## 11. Android Integration Guide

This API is designed to be consumed by an Android app using **Retrofit**.

### Retrofit Setup (Android)

**Add to `build.gradle`:**
```kotlin
implementation("com.squareup.retrofit2:retrofit:2.9.0")
implementation("com.squareup.retrofit2:converter-gson:2.9.0")
```

**Data class (matches `ItemResponse`):**
```kotlin
data class Item(
    val id: Int,
    val name: String,
    val description: String?
)

data class ItemCreate(
    val name: String,
    val description: String? = null
)
```

**API Interface:**
```kotlin
interface ItemsApi {
    @GET("api/items")
    suspend fun getAllItems(): List<Item>

    @GET("api/items/{id}")
    suspend fun getItem(@Path("id") id: Int): Item

    @POST("api/items")
    suspend fun createItem(@Body item: ItemCreate): Item

    @DELETE("api/items/{id}")
    suspend fun deleteItem(@Path("id") id: Int): Response<Unit>
}
```

**Retrofit Instance:**
```kotlin
val retrofit = Retrofit.Builder()
    .baseUrl("https://python-fastapi-demo-xxxx.onrender.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(ItemsApi::class.java)
```

---

*Documentation generated for python-fastapi-demo — FastAPI Items API*
