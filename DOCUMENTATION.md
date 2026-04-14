# My Notebook API — Full Documentation

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
10. [Deployment Guide (Render + Supabase)](#10-deployment-guide-render--supabase)
11. [Android Integration Guide](#11-android-integration-guide)

---

## 1. Project Overview

**python-fastapi-demo** is a personal notebook REST API.
Write your topics, stories and thoughts — all stored permanently in a PostgreSQL database on Supabase.

Built to showcase:
- Clean Python API architecture with FastAPI
- Automatic API documentation via Swagger UI
- PostgreSQL via Supabase for permanent cloud storage
- SQLite for zero-setup local development
- Production deployment on Render

**Live API:** https://python-fastapi-demo-vfm6.onrender.com

**Swagger Docs:** https://python-fastapi-demo-vfm6.onrender.com/docs

---

## 2. Tech Stack

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11 | Programming language |
| FastAPI | 0.115.6 | Web framework for building APIs |
| SQLAlchemy | 2.0.36 | ORM — talks to database using Python objects |
| Pydantic | 2.10.3 | Data validation and serialization |
| psycopg2-binary | 2.9.10 | PostgreSQL driver for Python |
| Uvicorn | 0.32.1 | ASGI server — runs the FastAPI app |
| SQLite | Built-in | Local database (file-based, zero setup) |
| Supabase | — | PostgreSQL database (production) |
| Render | — | Cloud hosting platform |

---

## 3. Project Structure

```
python-fastapi-demo/
│
├── main.py           → API entry point and route definitions
├── database.py       → Database connection and session management
├── models.py         → SQLAlchemy Note model
├── schemas.py        → Pydantic request/response schemas
├── requirements.txt  → Python package dependencies
├── runtime.txt       → Python version for Render
├── .python-version   → Python version for Render (newer standard)
├── .gitignore        → Files excluded from GitHub
├── README.md         → Quick start guide
├── DOCUMENTATION.md  → This file — full project documentation
│
├── items.db          → SQLite database file (local only, not on GitHub)
└── venv/             → Python virtual environment (not on GitHub)
```

---

## 4. File Breakdown

### `main.py`
The entry point of the application.

**Responsibilities:**
- Creates the FastAPI app instance with title, description, version
- Creates all database tables on startup (`Base.metadata.create_all`)
- Seeds 2 default notes on first run if the database is empty
- Defines all 7 API route handlers

**Key dependencies imported:**
- `database.py` → `engine`, `get_db`, `Base`
- `models.py` → `Note`
- `schemas.py` → `NoteCreate`, `NoteResponse`

---

### `database.py`
Manages the database connection and session lifecycle.

**Responsibilities:**
- Reads `DATABASE_URL` from environment variable (falls back to SQLite locally)
- Fixes `postgres://` → `postgresql://` prefix for SQLAlchemy compatibility
- Creates the SQLAlchemy engine
- Creates `SessionLocal` — a factory for database sessions
- Defines `Base` — the parent class all models inherit from
- Provides `get_db()` — a dependency that opens and closes DB sessions per request

---

### `models.py`
Defines the database table structure using SQLAlchemy.

**Table: `notes`**

| Column | Type | Constraints |
|---|---|---|
| id | Integer | Primary key, auto-increment, indexed |
| title | String | Not null |
| content | Text | Nullable (optional) |
| created_at | DateTime | Auto-set by database on insert |

---

### `schemas.py`
Defines the shape of data going in and out of the API using Pydantic.

**Schemas:**
- `NoteCreate` — validates incoming POST/PUT request body
- `NoteResponse` — shapes outgoing JSON responses (includes `id` and `created_at`)

---

### `requirements.txt`
Lists all Python packages needed to run the project.

```
fastapi==0.115.6
uvicorn==0.32.1
sqlalchemy==2.0.36
pydantic==2.10.3
psycopg2-binary==2.9.10
```

---

## 5. Database Design

### Table: `notes`

```
┌────┬──────────────┬───────────────────────────┬─────────────────────────┐
│ id │    title     │          content          │        created_at       │
│ int│   string     │           text            │        datetime         │
│ PK │  NOT NULL    │         NULLABLE          │     AUTO (server)       │
├────┼──────────────┼───────────────────────────┼─────────────────────────┤
│  1 │ Welcome      │ This is my personal...    │ 2026-04-14 10:00:00     │
│  2 │ First Story  │ Today was a great day...  │ 2026-04-14 10:00:01     │
└────┴──────────────┴───────────────────────────┴─────────────────────────┘
```

These 2 rows are **seeded automatically** on the first run if the database is empty.

---

## 6. API Endpoints

### Base URLs
```
Local:      http://127.0.0.1:8000
Production: https://python-fastapi-demo-vfm6.onrender.com
```

---

### `GET /`
Health check — confirms the API is running.

**Response:**
```json
{ "message": "My Notebook API is running!" }
```

---

### `GET /api/notes`
Returns all notes ordered by newest first.

**Response `200 OK`:**
```json
[
  {
    "id": 2,
    "title": "First Story",
    "content": "Today was a great day...",
    "created_at": "2026-04-14T10:00:01Z"
  },
  {
    "id": 1,
    "title": "Welcome",
    "content": "This is my personal notebook...",
    "created_at": "2026-04-14T10:00:00Z"
  }
]
```

---

### `GET /api/notes/{note_id}`
Returns a single note by ID.

**Response `200 OK`:**
```json
{
  "id": 1,
  "title": "Welcome",
  "content": "This is my personal notebook...",
  "created_at": "2026-04-14T10:00:00Z"
}
```

**Response `404 Not Found`:**
```json
{ "detail": "Note not found" }
```

---

### `POST /api/notes`
Creates a new note.

**Request body:**
```json
{
  "title": "My Topic",
  "content": "My story goes here..."
}
```
> `content` is optional. `title` is required.

**Response `201 Created`:**
```json
{
  "id": 3,
  "title": "My Topic",
  "content": "My story goes here...",
  "created_at": "2026-04-14T15:30:00Z"
}
```

---

### `PUT /api/notes/{note_id}`
Updates an existing note.

**Request body:**
```json
{
  "title": "Updated Topic",
  "content": "Updated story..."
}
```

**Response `200 OK`:** returns the updated note

**Response `404 Not Found`:**
```json
{ "detail": "Note not found" }
```

---

### `DELETE /api/notes/{note_id}`
Deletes a single note by ID.

**Response `204 No Content`:** (empty body — success)

**Response `404 Not Found`:**
```json
{ "detail": "Note not found" }
```

---

### `DELETE /api/notes`
Deletes multiple notes at once.

**Request body:**
```json
{
  "ids": [1, 2, 3]
}
```

**Response `200 OK`:**
```json
{
  "deleted": 3,
  "ids": [1, 2, 3]
}
```

---

## 7. Request & Response Schemas

### NoteCreate (Request — POST / PUT)
```json
{
  "title": "string (required)",
  "content": "string or null (optional)"
}
```

### NoteResponse (Response)
```json
{
  "id": "integer",
  "title": "string",
  "content": "string or null",
  "created_at": "datetime (ISO 8601)"
}
```

### BulkDeleteRequest (Request — DELETE /api/notes)
```json
{
  "ids": [1, 2, 3]
}
```

---

## 8. How to Run Locally

### Prerequisites
- Python 3.11 or higher
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
```
http://127.0.0.1:8000/docs
```
Click any endpoint → "Try it out" → "Execute" → see live response.

### Option 2 — Postman
- Set method (GET/POST/PUT/DELETE)
- Set URL
- For POST/PUT: Body → raw → JSON

### Option 3 — curl (Terminal)

```bash
# Get all notes
curl https://python-fastapi-demo-vfm6.onrender.com/api/notes

# Get one note
curl https://python-fastapi-demo-vfm6.onrender.com/api/notes/1

# Create a note
curl -X POST https://python-fastapi-demo-vfm6.onrender.com/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "My Topic", "content": "My story..."}'

# Update a note
curl -X PUT https://python-fastapi-demo-vfm6.onrender.com/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Topic", "content": "Updated story..."}'

# Delete one note
curl -X DELETE https://python-fastapi-demo-vfm6.onrender.com/api/notes/1

# Delete multiple notes
curl -X DELETE https://python-fastapi-demo-vfm6.onrender.com/api/notes \
  -H "Content-Type: application/json" \
  -d '{"ids": [1, 2, 3]}'
```

---

## 10. Deployment Guide (Render + Supabase)

### Step 1 — Create Supabase database
1. Go to [supabase.com](https://supabase.com) → sign up with GitHub
2. New Project → set name and password
3. Settings → Database → Connection Pooling → copy URI
4. Replace `[YOUR-PASSWORD]` in the URI with your actual password

### Step 2 — Push code to GitHub
```bash
git add .
git commit -m "your message"
git push
```

### Step 3 — Create Web Service on Render
1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect GitHub repo → select `python-fastapi-demo`
3. Configure:

| Field | Value |
|---|---|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Plan | Free |

### Step 4 — Add environment variable on Render

| Key | Value |
|---|---|
| `DATABASE_URL` | Your Supabase connection string |

### Step 5 — Deploy
Click **Create Web Service** → wait 2-3 minutes → your API is live.

> **Note:** Free tier sleeps after 15 mins of inactivity. First request after sleep takes ~30 seconds.

---

## 11. Android Integration Guide

### Retrofit Setup

**Add to `build.gradle`:**
```kotlin
implementation("com.squareup.retrofit2:retrofit:2.9.0")
implementation("com.squareup.retrofit2:converter-gson:2.9.0")
```

**Data classes:**
```kotlin
data class Note(
    val id: Int,
    val title: String,
    val content: String?,
    val created_at: String
)

data class NoteCreate(
    val title: String,
    val content: String? = null
)

data class BulkDeleteRequest(
    val ids: List<Int>
)
```

**API Interface:**
```kotlin
interface NotesApi {
    @GET("api/notes")
    suspend fun getAllNotes(): List<Note>

    @GET("api/notes/{id}")
    suspend fun getNote(@Path("id") id: Int): Note

    @POST("api/notes")
    suspend fun createNote(@Body note: NoteCreate): Note

    @PUT("api/notes/{id}")
    suspend fun updateNote(@Path("id") id: Int, @Body note: NoteCreate): Note

    @DELETE("api/notes/{id}")
    suspend fun deleteNote(@Path("id") id: Int): Response<Unit>

    @DELETE("api/notes")
    suspend fun deleteNotesBulk(@Body request: BulkDeleteRequest): Response<Unit>
}
```

**Retrofit Instance:**
```kotlin
val retrofit = Retrofit.Builder()
    .baseUrl("https://python-fastapi-demo-vfm6.onrender.com/")
    .addConverterFactory(GsonConverterFactory.create())
    .build()

val api = retrofit.create(NotesApi::class.java)
```

---

*Documentation for python-fastapi-demo — My Notebook API*
