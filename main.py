from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, Base
from models import Item
from schemas import ItemCreate, ItemResponse

app = FastAPI(
    title="Items API",
    description="Simple Items API - Interview Demo",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def seed_data():
    db = next(get_db())
    if db.query(Item).count() == 0:
        db.add_all([
            Item(name="MacBook Pro", description="Apple laptop"),
            Item(name="iPhone 16", description="Apple smartphone"),
            Item(name="Samsung Galaxy S25", description="Android smartphone"),
            Item(name="Sony WH-1000XM5", description="Noise cancelling headphones"),
            Item(name="iPad Pro", description="Apple tablet"),
        ])
        db.commit()


@app.get("/")
def root():
    return {"message": "Items API is running!"}


@app.get("/api/items", response_model=List[ItemResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()


@app.get("/api/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/api/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    new_item = Item(name=item.name, description=item.description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
