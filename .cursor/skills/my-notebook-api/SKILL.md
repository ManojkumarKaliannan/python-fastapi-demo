---
name: my-notebook-api
description: Provides full context about Manojka's "My Notebook API" FastAPI project so the agent can make changes without re-explanation. Use when the user says "add this", "delete that", "change the endpoint", "update the model", or any short instruction about the notebook API project without providing background.
---

# My Notebook API — Project Context

## Project Summary
Personal REST API for storing notes (topics, stories, thoughts). Built with FastAPI + SQLAlchemy. Deployed on Render with Supabase PostgreSQL in production.

- **Repo:** `python-fastapi-demo` at `/Users/manojka/Documents/GitHub/python-fastapi-demo`
- **Live API:** https://python-fastapi-demo-vfm6.onrender.com
- **Swagger docs:** https://python-fastapi-demo-vfm6.onrender.com/docs

## File Structure

```
main.py        # FastAPI app, all routes, startup seed
database.py    # SQLAlchemy engine, session, Base
models.py      # Note SQLAlchemy model
schemas.py     # Pydantic schemas (NoteCreate, NoteResponse)
requirements.txt
runtime.txt
.gitignore
items.db       # SQLite (local dev only)
```

## Tech Stack

| Layer | Tool |
|---|---|
| Framework | FastAPI 0.115.6 |
| ORM | SQLAlchemy 2.0.36 |
| Validation | Pydantic 2.10.3 |
| Server | Uvicorn 0.32.1 |
| DB (local) | SQLite (`items.db`) |
| DB (prod) | PostgreSQL via Supabase |
| Hosting | Render |
| DB driver | psycopg2-binary 2.9.10 |

## Database Model — `Note`

```python
class Note(Base):
    __tablename__ = "notes"
    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String, nullable=False)
    content    = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

## Pydantic Schemas

```python
class NoteCreate(BaseModel):
    title: str
    content: str | None = None

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str | None = None
    created_at: datetime
    class Config:
        from_attributes = True
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/api/notes` | All notes (newest first) |
| GET | `/api/notes/{id}` | Single note |
| POST | `/api/notes` | Create note |
| PUT | `/api/notes/{id}` | Update note |
| DELETE | `/api/notes/{id}` | Delete single note |
| DELETE | `/api/notes` | Bulk delete by `{"ids": [1,2,3]}` |

## Database Setup (database.py)

- Reads `DATABASE_URL` env var; defaults to SQLite locally
- Auto-converts `postgres://` → `postgresql://` for SQLAlchemy compatibility
- SQLite uses `check_same_thread=False`; PostgreSQL does not

## Deployment

- **Platform:** Render
- **Build:** `pip install -r requirements.txt`
- **Start:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Env var:** `DATABASE_URL` = Supabase connection string

## Key Conventions

- All note routes are prefixed `/api/notes`
- Responses ordered newest first (`order_by(Note.created_at.desc())`)
- 404 raised with `detail="Note not found"` when note missing
- Startup seed adds 2 default notes if DB is empty
- Bulk delete returns `{"deleted": count, "ids": [...]}`
