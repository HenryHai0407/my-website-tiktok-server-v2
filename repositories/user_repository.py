from typing import List
from sqlmodel import Session, select
from models.auth_model import AuthModel
from models.user_model import UserModel
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, model_user: UserModel, model_auth: AuthModel) -> UserModel:
        self.db.add(model_auth)
        self.db.flush()

        model_user.auth_id = model_auth.id
        self.db.add(model_user)

        self.db.commit()
        self.db.refresh(model_user)

        return model_user

    def get_by_username(self, username: str) -> UserModel | None:
        statement = select(UserModel).join(
            AuthModel).where(AuthModel.username == username)
        model = self.db.exec(statement).first()
        return model

    def get_list(self) -> List[UserModel]:
        statement = select(UserModel).join(AuthModel).where(
            AuthModel.delete_flg == False, AuthModel.is_active == True)
        return self.db.exec(statement).all()

    def get_by_id(self, id: int) -> UserModel:
        statement = select(UserModel).join(AuthModel).where(UserModel.id == id)
        return self.db.exec(statement).one()

    def update(self, model: UserModel) -> UserModel:
        self.db.commit()
        self.db.refresh(model)
        return model

    def delete(self, model: UserModel) -> UserModel:
        self.db.commit()
        self.db.refresh(model)
        return model
