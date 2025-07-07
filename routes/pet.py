from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.pet import Pet
from schemas.pet import PetSchema
from db import get_db
from typing import List, Optional

router = APIRouter()

# CRUD for Pet







@router.post("/", response_model=PetSchema)
async def create_pet(item: PetSchema, db: Session = Depends(get_db)):
    db_item = Pet(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@router.get("/", response_model=List[PetSchema])
async def read_pets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Pet).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=PetSchema)
async def read_pet(id: int, db: Session = Depends(get_db)):
    item = db.query(Pet).filter(Pet.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return item




@router.put("/{id}", response_model=PetSchema)
async def update_pet(id: int, updated: PetSchema, db: Session = Depends(get_db)):
    db_item = db.query(Pet).filter(Pet.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item



@router.delete("/{id}")
async def delete_pet(id: int, db: Session = Depends(get_db)):
    db_item = db.query(Pet).filter(Pet.id == id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "Pet deleted successfully"}
