from fastapi import APIRouter, Depends, Request
from sqlmodel import Session
from databases.db_mysql import get_db_session
from services.user_service import UserService
from services.auth_service import AuthService
from models.user_model import UserDTO, UserDTOCreate
from models.auth_model import AuthLoginRequest, AuthLoginResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserDTO)
def create(request: Request, req: UserDTOCreate, db: Session = Depends(get_db_session)):
    service = UserService(db)
    return service.create(req)


@router.post("/login", response_model=AuthLoginResponse)
def create(request: Request, req: AuthLoginRequest, db: Session = Depends(get_db_session)):
    service = AuthService(db)
    return service.login(req)
