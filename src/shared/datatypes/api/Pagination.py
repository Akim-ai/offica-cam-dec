from typing import Iterable, Any, Union

from pydantic import BaseModel, NonNegativeInt
from sqlalchemy import CursorResult, Result


class PaginatorPage(BaseModel):
    page: NonNegativeInt = 1


class Paginator(PaginatorPage):
    data: list
    next: bool = False
    count: NonNegativeInt = 0

    @classmethod
    def assign(cls, objects: Union[CursorResult, Result], assigner: lambda x: x, cnt=0, offset=0, page=1, excluded=None) -> dict:
        _next: bool = False
        data = objects.all()

        print(data)
        if not data:
            return {'error': 'doesnt exists'}

        if not excluded:
            excluded = {}
        result = [assigner(_object).model_dump(exclude=excluded) for _object in data]

        if offset*page < cnt:
            _next = True

        return {
            'data': result,
            'next': _next,
            'count': cnt,
        }
