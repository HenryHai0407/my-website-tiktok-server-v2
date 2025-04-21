from fastapi import APIRouter, Depends, Request, Query
from fastapi.security import HTTPBearer
from sqlmodel import Session
from models.product_model import ProductDTO, ProductDTOCreate, ProductDTOUpdate
from services.product_service import ProductService
from databases.db_mysql import get_db_session
from typing import List, Optional

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    # dependencies=[Depends(HTTPBearer())]
)

@router.get("/hot_product", response_model=List[ProductDTO])
def get_hot(request: Request, db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.get_by_hot_product()

@router.get("/", response_model=List[ProductDTO])
def get_list(request: Request, hot_flg: Optional[int] = None, recommend_flg: Optional[int] = None, db: Session = Depends(get_db_session)):
    # print(request.state.user)
    service = ProductService(db)
    return service.get_list(hot_flg, recommend_flg)

@router.get("/search", response_model=List[ProductDTO])
def search_products(q:str = Query(...,alias="q"), db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.search_by_name_or_summary(q)
# This search endpoint should be placed before /{id}

@router.get("/{id}", response_model=ProductDTO)
def get_by_id(request: Request, id: int, db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.get_by_id(id)


@router.post("/", dependencies=[Depends(HTTPBearer())], response_model=ProductDTO)
def create(request: Request, req: ProductDTOCreate, db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.create(req)


@router.put("/{id}", dependencies=[Depends(HTTPBearer())], response_model=ProductDTO)
def update(request: Request, id: int, req: ProductDTOUpdate, db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.update(id, req)


@router.delete("/{id}", dependencies=[Depends(HTTPBearer())])
def delete(request: Request, id: int, db: Session = Depends(get_db_session)):
    service = ProductService(db)
    return service.delete(id)

