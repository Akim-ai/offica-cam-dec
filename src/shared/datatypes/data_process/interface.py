from pydantic import BaseModel, NonNegativeInt


class IDataProcessFrameProcessFactory(BaseModel):
    id_: NonNegativeInt

    def __init__(self, id_):
        super().__init__(id_=id_)
        self.id_ = id_


class IDataProcessFrameProcessFactoryList(BaseModel):
    frame_processors: list[IDataProcessFrameProcessFactory] = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_processors = self.frame_processors if self.frame_processors else []
