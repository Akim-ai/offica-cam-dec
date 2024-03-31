from pydantic import BaseModel, NonNegativeInt


class IDataGetFactory(BaseModel):
    id_: NonNegativeInt
    local_address: str

    def __init__(self, id_: int, local_address: str):
        super().__init__(id_=id_, local_address=local_address)
        self.id_ = id_
        self.local_address = local_address


class IDataGetFactoryList(BaseModel):
    data_get_factory_data: list[IDataGetFactory] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_get_factory_data = self.data_get_factory_data if self.data_get_factory_data else []
