from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.apiresponse import ApiResponse
from schemas.apiresponse import ApiResponseSchema
from db import get_db
from typing import List, Optional

router = APIRouter()

# CRUD for ApiResponse







@router.post("/", response_model=ApiResponseSchema)
async def create_apiresponse(item: ApiResponseSchema, db: Session = Depends(get_db)):
    db_item = ApiResponse(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



@router.get("/", response_model=List[ApiResponseSchema])
async def read_apiresponses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(ApiResponse).offset(skip).limit(limit).all()


@router.get("/{code}", response_model=ApiResponseSchema)
async def read_apiresponse(code: int, db: Session = Depends(get_db)):
    item = db.query(ApiResponse).filter(ApiResponse.code == code).first()
    if item is None:
        raise HTTPException(status_code=404, detail="ApiResponse not found")
    return item




@router.put("/{code}", response_model=ApiResponseSchema)
async def update_apiresponse(code: int, updated: ApiResponseSchema, db: Session = Depends(get_db)):
    db_item = db.query(ApiResponse).filter(ApiResponse.code == code).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="ApiResponse not found")
    for key, value in updated.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item



@router.delete("/{code}")
async def delete_apiresponse(code: int, db: Session = Depends(get_db)):
    db_item = db.query(ApiResponse).filter(ApiResponse.code == code).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="ApiResponse not found")
    db.delete(db_item)
    db.commit()
    return {"detail": "ApiResponse deleted successfully"}
