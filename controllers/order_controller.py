from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlmodel import Session
from typing import List
from services.order_service import OrderService
from databases.db_mysql import get_db_session
from models.order_model import OrderDTO, OrderDTOCreate

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(HTTPBearer())]
)


@router.post("/", response_model=OrderDTO)
def create_order(request: Request, req: OrderDTOCreate, db: Session = Depends(get_db_session)):
    service = OrderService(db)
    return service.create(req)


@router.get("/", response_model=List[OrderDTO])
def get_list(request: Request, db: Session = Depends(get_db_session)):
    service = OrderService(db)
    return service.get_list()


@router.get("/{order_id}", response_model=OrderDTO)
def get_by_id(request: Request, order_id: int, db: Session = Depends(get_db_session)):
    service = OrderService(db)
    return service.get_by_id(order_id)
