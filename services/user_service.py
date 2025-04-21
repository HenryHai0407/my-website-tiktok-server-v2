from typing import List
from sqlmodel import Session
from repositories.user_repository import UserRepository
from models.user_model import UserModel, UserDTO, UserDTOCreate, UserDTOUpdate
from models.auth_model import AuthModel
from utils.security_util import SecurityUtil
from exceptions.custom_exception import AppException, ExceptionType


class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(self.db)

    def create(self, dto: UserDTOCreate) -> UserDTO:
        model = self.repo.get_by_username(dto.username)
        if model:
            raise AppException(ExceptionType.ALREADY_EXISTS)

        model_auth = AuthModel(**dto.model_dump())
        model_user = UserModel(**dto.model_dump())
        model_auth.password = SecurityUtil.hash_password(dto.password)

        return self.repo.create(model_user, model_auth)

    def get_list(self) -> List[UserDTO]:
        items = self.repo.get_list()
        return [UserDTO.model_validate(i) for i in items]

    def get_by_id(self, id: int) -> UserDTO:
        item = self.repo.get_by_id(id)
        return UserDTO.model_validate(item)

    def update(self, id: int, dto: UserDTOUpdate) -> UserDTO:
        model = self.repo.get_by_id(id)
        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(model, field, value)

        model = self.repo.update(model)

        return UserDTO.model_validate(model)

    def delete(self, id: int) -> UserDTO:
        model = self.repo.get_by_id(id)
        if not model:
            raise AppException(ExceptionType.NOT_FOUND)

        model.delete_flg = True
        model.auth.delete_flg = True
        model = self.repo.delete(model)

        return UserDTO.model_validate(model)
