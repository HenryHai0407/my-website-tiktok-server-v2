from sqlmodel import Session
from models.category_model import CategoryModel, CategoryDTO, CategoryDTOCreate, CategoryDTOUpdate
from repositories.category_repository import CategoryRepository
from typing import List
from exceptions.custom_exception import AppException, ExceptionType


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = CategoryRepository(self.db)

    def get_list(self) -> List[CategoryDTO]:
        models = self.repo.get_list()
        return [CategoryDTO.model_validate(model) for model in models]

    def get_by_id(self, id: int) -> CategoryDTO:
        model = self.repo.get_by_id(id)
        return CategoryDTO.model_validate(model)

    def create(self, dto: CategoryDTOCreate) -> CategoryDTO:
        model = CategoryModel(**dto.model_dump())
        model = self.repo.create(model)

        return CategoryDTO.model_validate(model)

    def update(self, id: int, dto: CategoryDTOUpdate) -> CategoryDTO:
        model = self.repo.get_by_id(id)
        if not model:
            raise AppException(ExceptionType.NOT_FOUND)

        model.name = dto.name
        model.description = dto.description
        self.repo.update(model)

        return CategoryDTO.model_validate(model)

    def delete(self, id: int) -> None:
        model = self.repo.get_by_id(id)
        if not model:
            raise AppException(ExceptionType.NOT_FOUND)

        self.repo.delete(model)
