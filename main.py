from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from database import engine, get_db, Base
from models import Note
from schemas import NoteCreate, NoteResponse

app = FastAPI(
    title="My Notebook API",
    description="Personal Notebook — store your topics and stories",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def seed_data():
    db = next(get_db())
    if db.query(Note).count() == 0:
        db.add_all([
            Note(title="Welcome", content="This is my personal notebook. I will write my thoughts, stories and ideas here."),
            Note(title="First Story", content="Today was a great day. I built and deployed my first FastAPI backend to Render!"),
        ])
        db.commit()


@app.get("/")
def root():
    return {"message": "My Notebook API is running!"}


@app.get("/api/notes", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db)):
    return db.query(Note).order_by(Note.created_at.desc()).all()


@app.get("/api/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.post("/api/notes", response_model=NoteResponse, status_code=201)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note


@app.put("/api/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, updated: NoteCreate, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = updated.title
    note.content = updated.content
    db.commit()
    db.refresh(note)
    return note


@app.delete("/api/notes/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()


class BulkDeleteRequest(BaseModel):
    ids: List[int]


@app.delete("/api/notes", status_code=200)
def delete_notes_bulk(request: BulkDeleteRequest, db: Session = Depends(get_db)):
    deleted = db.query(Note).filter(Note.id.in_(request.ids)).all()
    if not deleted:
        raise HTTPException(status_code=404, detail="No notes found with given ids")
    for note in deleted:
        db.delete(note)
    db.commit()
    return {"deleted": len(deleted), "ids": request.ids}
