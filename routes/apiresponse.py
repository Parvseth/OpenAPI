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
    db_item = ApiResponse(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item






