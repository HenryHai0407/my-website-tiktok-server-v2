from sqlmodel import Session, select
from models.category_model import CategoryModel
from typing import List


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list(self) -> List[CategoryModel]:
        statement = select(CategoryModel)
        # result = self.db.execute(statement).scalars()
        result = self.db.exec(statement)
        return result.all()

    def get_by_id(self, id: int) -> CategoryModel:
        result = self.db.get(CategoryModel, id)
        return result

    def create(self, model: CategoryModel) -> CategoryModel:
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return model

    def update(self, model: CategoryModel) -> CategoryModel:
        self.db.commit()
        self.db.refresh(model)
        return model

    def delete(self, model: CategoryModel) -> None:
        self.db.delete(model)
        self.db.commit()
