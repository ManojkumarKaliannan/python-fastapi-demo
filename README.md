# Items API — FastAPI Demo

A simple RESTful API built with **FastAPI** and **SQLAlchemy**, demonstrating CRUD operations on an Items resource. Uses SQLite for local development and can be swapped to PostgreSQL for production.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [Pydantic](https://docs.pydantic.dev/) — data validation
- SQLite (local) / PostgreSQL (production)

---

## Getting Started (Local)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/python-fastapi-demo.git
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
| `GET` | `/api/items` | List all items |
| `GET` | `/api/items/{id}` | Get a single item |
| `POST` | `/api/items` | Create a new item |
| `DELETE` | `/api/items/{id}` | Delete an item |

### Example Request

```bash
# Create an item
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "AirPods Pro", "description": "Apple wireless earbuds"}'
```

---

## Deploying to Render

### 1. Push your code to GitHub

Make sure your `.gitignore` is committed so that `venv/` and `*.db` are excluded.

### 2. Create a new Web Service on Render

1. Go to [render.com](https://render.com) and click **New → Web Service**.
2. Connect your GitHub repository.
3. Fill in the settings:

| Setting | Value |
|---------|-------|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

### 3. (Optional) Switch to PostgreSQL

Render provides a managed PostgreSQL database. Once created, copy the **Internal Database URL** and set it as an environment variable:

```
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

Then update `database.py` to read from the environment:

```python
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./items.db")
```

---

## Project Structure

```
python-fastapi-demo/
├── main.py          # FastAPI app, routes, and startup seed
├── database.py      # Database engine and session setup
├── models.py        # SQLAlchemy ORM models
├── schemas.py       # Pydantic request/response schemas
├── requirements.txt # Python dependencies
└── .gitignore
```

---

## License

MIT
