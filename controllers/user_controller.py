from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlmodel import Session
from typing import List
from databases.db_mysql import get_db_session
from services.user_service import UserService
from models.user_model import UserDTO, UserDTOUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(HTTPBearer())]
)


@router.get("/profile", response_model=UserDTO)
def get_profile(request: Request, db: Session = Depends(get_db_session)):
    return request.state.user


@router.get("/", response_model=List[UserDTO])
def get_list(request: Request, db: Session = Depends(get_db_session)):
    print(request.state.user)
    service = UserService(db)
    return service.get_list()


@router.get("/{id}", response_model=UserDTO)
def get_by_id(request: Request, id: int, db: Session = Depends(get_db_session)):
    service = UserService(db)
    return service.get_by_id(id)


@router.put("/{id}", response_model=UserDTO)
def update(request: Request, id: int, req: UserDTOUpdate, db: Session = Depends(get_db_session)):
    service = UserService(db)
    return service.update(id, req)


@router.delete("/{id}", response_model=UserDTO)
def update(request: Request, id: int, db: Session = Depends(get_db_session)):
    service = UserService(db)
    return service.delete(id)
