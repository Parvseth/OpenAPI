from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.order import Order
from schemas.order import OrderSchema
from db import get_db
from typing import List, Optional

router = APIRouter()

# CRUD for Order







@router.post("/", response_model=OrderSchema)
async def create_order(item: OrderSchema, db: Session = Depends(get_db)):
    db_item = Order(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@router.get("/", response_model=List[OrderSchema])
async def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Order).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=OrderSchema)
async def read_order(id: int, db: Session = Depends(get_db)):
    item = db.query(Order).filter(Order.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return item





