# My Notebook API — FastAPI

A personal notebook REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL (Supabase)**. Write your topics, stories and thoughts — all stored permanently in the cloud.

Live API: [https://python-fastapi-demo-vfm6.onrender.com](https://python-fastapi-demo-vfm6.onrender.com)

Swagger Docs: [https://python-fastapi-demo-vfm6.onrender.com/docs](https://python-fastapi-demo-vfm6.onrender.com/docs)

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [Pydantic](https://docs.pydantic.dev/) — data validation
- [Supabase](https://supabase.com/) — PostgreSQL database (production)
- SQLite — local development
- [Render](https://render.com/) — hosting

---

## Getting Started (Local)

### 1. Clone the repo

```bash
git clone https://github.com/ManojkumarKaliannan/python-fastapi-demo.git
cd python-fastapi-demo
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive docs (Swagger UI): `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/api/notes` | Get all notes (newest first) |
| `GET` | `/api/notes/{id}` | Get a single note |
| `POST` | `/api/notes` | Create a new note |
| `PUT` | `/api/notes/{id}` | Update an existing note |
| `DELETE` | `/api/notes/{id}` | Delete a single note |
| `DELETE` | `/api/notes` | Delete multiple notes by IDs |

### Create a note

```bash
curl -X POST https://python-fastapi-demo-vfm6.onrender.com/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title": "My Topic", "content": "My story goes here..."}'
```

### Update a note

```bash
curl -X PUT https://python-fastapi-demo-vfm6.onrender.com/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Topic", "content": "Updated story..."}'
```

### Delete multiple notes

```bash
curl -X DELETE https://python-fastapi-demo-vfm6.onrender.com/api/notes \
  -H "Content-Type: application/json" \
  -d '{"ids": [1, 2, 3]}'
```

---

## Project Structure

```
python-fastapi-demo/
├── main.py          # FastAPI app, routes, and startup seed
├── database.py      # Database engine and session setup
├── models.py        # Note model (id, title, content, created_at)
├── schemas.py       # Pydantic request/response schemas
├── requirements.txt # Python dependencies
├── runtime.txt      # Python version for Render
├── .python-version  # Python version for Render
└── .gitignore
```

---

## Deploying to Render

### 1. Push code to GitHub

```bash
git add .
git commit -m "your message"
git push
```

### 2. Create Web Service on Render

| Setting | Value |
|---------|-------|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

### 3. Add environment variable

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your Supabase connection string |

---

## Database

- **Local:** SQLite (`items.db`) — zero setup
- **Production:** PostgreSQL via [Supabase](https://supabase.com) — free, permanent storage

The app automatically uses SQLite locally and PostgreSQL on Render via the `DATABASE_URL` environment variable.

---

## License

MIT
