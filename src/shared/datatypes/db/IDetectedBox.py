from datetime import datetime
from typing import Optional

from pydantic import BaseModel, NonNegativeInt

from src.Database.Models import DetectedBox


class IDetectedBox(BaseModel):
    id: Optional[NonNegativeInt]
    frame: NonNegativeInt

    top_x: int
    top_y: int
    bot_x: int
    bot_y: int

    created_at: datetime

    def __init__(self, top_x: int, top_y: int, bot_x: int, bot_y: int, frame: int, *args, **kwargs):
        self.top_x = top_x
        self.top_y = top_y
        self.bot_x = bot_x
        self.bot_y = bot_y

        self.frame = frame

        super().__init__(top_x=top_x, top_y=top_y, bot_x=bot_x, bot_y=bot_y, frame=frame)

        self.model_validate(self)

    @staticmethod
    def __assign_fields(obj_from, obj_to):
        obj_to.top_x = obj_from.top_x
        obj_to.top_y = obj_from.top_y
        obj_to.bot_x = obj_from.bot_x
        obj_to.bot_y = obj_from.bot_y

        obj_to.frame = obj_from.frame

    @classmethod
    def from_db_detected_box(cls, frame: DetectedBox) -> 'IDetectedBox':
        self = cls.__new__(cls=cls)
        self.__assign_fields(obj_to=self, obj_from=frame)
        return self

    def to_db_detected_box(self) -> DetectedBox:
        detected_box: DetectedBox = DetectedBox()

        self.__assign_fields(obj_to=detected_box, obj_from=self)

        return detected_box


class IDetectedBoxList:
    boxes: list[IDetectedBox] = None

    def append_box(self, box: IDetectedBox):
        if not self.boxes:
            self.boxes = []
        self.boxes.append(box)

