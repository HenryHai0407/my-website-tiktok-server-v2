from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from sqlmodel import Session
from models.category_model import CategoryDTO, CategoryDTOCreate, CategoryDTOUpdate
from services.category_service import CategoryService
from databases.db_mysql import get_db_session
from typing import List

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    # dependencies=[Depends(HTTPBearer())]
)


@router.get("/", response_model=List[CategoryDTO])
def get_list(request: Request, db: Session = Depends(get_db_session)):
    # print(request.state.user)
    service = CategoryService(db)
    return service.get_list()


@router.get("/{id}", response_model=CategoryDTO)
def get_by_id(request: Request, id: int, db: Session = Depends(get_db_session)):
    service = CategoryService(db)
    return service.get_by_id(id)


@router.post("/", dependencies=[Depends(HTTPBearer())], response_model=CategoryDTO)
def create(request: Request, req: CategoryDTOCreate, db: Session = Depends(get_db_session)):
    service = CategoryService(db)
    return service.create(req)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())], response_model=CategoryDTO)
def update_product(request: Request, id: int, req: CategoryDTOUpdate, db: Session = Depends(get_db_session)):
    service = CategoryService(db)
    return service.update(id, req)


@router.delete("/{id}", dependencies=[Depends(HTTPBearer())])
def delete(request: Request, id: int, db: Session = Depends(get_db_session)):
    service = CategoryService(db)
    return service.delete(id)
