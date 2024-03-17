from typing import Type, Any
from abc import ABC

from sqlalchemy.orm import Session, Query

from .database import Base
from . import models


class BaseCrud(ABC):

    def __init__(self, model: Type[Base], db: Session) -> None:

        self.model = model
        self.db = db

    def _get_query(self) -> Query:
        return self.db.query(self.model)

    def _get_query_filtered(self, **kwargs) -> Query:
        return self._get_query().filter_by(**kwargs)

    @staticmethod
    def _get_as_list(object_to_get: Any) -> list[Any]:
        return object_to_get if isinstance(object_to_get, list) else [object_to_get]

    def refresh(self, objects_to_refresh: list[Type[Base]] | Type[Base]) -> None:
        for object_to_refresh in self._get_as_list(objects_to_refresh):
            self.db.refresh(object_to_refresh)

    def add_to_db_and_refresh(self, object_to_add: Type[Base]) -> None:

        self.db.add(object_to_add)
        self.db.commit()
        self.refresh(object_to_add)

    def create(self, **kwargs) -> Type[Base]:

        db_object = self.model(**kwargs)

        self.add_to_db_and_refresh(db_object)

        return db_object

    def get(self, **kwargs) -> Type[Base]:
        return self._get_query_filtered(**kwargs).first()

    def update(self, objects_to_update: Type[Base] | list[Type[Base]], **kwargs) -> None:

        objects_to_update = self._get_as_list(objects_to_update)

        for object_to_update in objects_to_update:
            for key, value in kwargs.items():
                setattr(object_to_update, key, value)

        self.db.commit()
        self.refresh(objects_to_update)


class UserCrud(BaseCrud):
    def __init__(self, db: Session) -> None:
        super().__init__(models.User, db)
