from typing import Any

from pydantic import BaseModel, NonNegativeInt

from src.shared.datatypes.CustomFields.HexBytes import HexBytes


class IUser(BaseModel):
    id: NonNegativeInt = 0
    password: str = None
    first_name: str
    last_name: str
    detected_path_image: str = ''

    def __repr__(self):
        return f'{self.id}-{self.first_name}-{self.last_name}'


class ListIUser(BaseModel):
    users: list[IUser] | list = []


class IUserWithImage(IUser):
    detected_image: HexBytes


class IListUserWithImage(BaseModel):
    users: list[IUserWithImage] | list = []