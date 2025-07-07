from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserSchema
from db import get_db
from typing import List, Optional

router = APIRouter()

# CRUD for User







@router.post("/", response_model=UserSchema)
async def create_user(item: UserSchema, db: Session = Depends(get_db)):
    db_item = User(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@router.get("/", response_model=List[UserSchema])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(User).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=UserSchema)
async def read_user(id: int, db: Session = Depends(get_db)):
    item = db.query(User).filter(User.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="User not found")
    return item




@router.put("/{id}", response_model=UserSchema)
async def update_user(id: int, updated: UserSchema, db: Session = Depends(get_db)):
    db_item = db.query(User).filter(User.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


