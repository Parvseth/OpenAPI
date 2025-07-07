from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.pet import Pet
from schemas.pet import PetSchema
from db import get_db
from typing import List, Optional

router = APIRouter()

# CRUD for Pet









@router.get("/", response_model=List[PetSchema])
async def read_pets(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Pet).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=PetSchema)
async def read_pet(id: int, db: Session = Depends(get_db)):
    item = db.query(Pet).filter(Pet.id == id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return item





