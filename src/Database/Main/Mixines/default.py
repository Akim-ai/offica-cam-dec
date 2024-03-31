import uuid

from sqlalchemy import UUID, Column, ForeignKey, Integer
from sqlalchemy.orm import declared_attr, Mapped, has_inherited_table


class CreateTableName:
    @declared_attr
    def __tablename__(cls) -> str:
        name: str = cls.__name__
        sql_name: str = name[0].lower()
        name = name[1:]
        for i, v in enumerate(name):
            if v.isupper():
                sql_name += f'__{name[i].lower()}'
                continue
            sql_name += f'{name[i]}'
        return sql_name


class UserHasIDMixin:
    @declared_attr
    def id(cls):
        if cls.__name__ != 'User':
            return Column('id', UUID, ForeignKey("user.id"), primary_key=True)
        else:
            return Column('id', type_=UUID, primary_key=True, default=uuid.uuid4(), unique=True)

