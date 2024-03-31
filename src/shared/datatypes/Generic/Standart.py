from pydantic import BaseModel, NonNegativeInt


class PositiveInt(BaseModel):
    value: NonNegativeInt

