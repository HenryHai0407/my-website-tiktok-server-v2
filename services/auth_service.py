from typing import List
from sqlmodel import Session
from repositories.user_repository import UserRepository
from models.user_model import UserDTO
from models.auth_model import AuthLoginRequest, AuthLoginResponse
from utils.security_util import SecurityUtil
from exceptions.custom_exception import AppException, ExceptionType


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(self.db)

    def login(self, dto: AuthLoginRequest) -> AuthLoginResponse:
        item = self.repo.get_by_username(dto.username)
        if not item:
            raise AppException(ExceptionType.UNAUTHORIZED)

        is_auth = SecurityUtil.verify_password(
            dto.password, item.auth.password)
        if not is_auth:
            raise AppException(ExceptionType.UNAUTHORIZED)

        payload = UserDTO.model_validate(item)
        token = SecurityUtil.generate_access_token(payload)

        return AuthLoginResponse(access_token=token)
