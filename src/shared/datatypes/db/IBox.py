from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, NonNegativeInt

from src.Database.Models import DetectedBox, Frame
from src.shared.datatypes.db.IFrame import IFrame
from src.shared.datatypes.json_encoders_decoders.datetime import \
    convert_datetime_to_iso_8601_with_z_suffix, transform_to_utc_datetime


class IBox(BaseModel):
    id: Optional[int] = None

    top_x: int
    top_y: int
    bot_x: int
    bot_y: int

    detected_user: Optional[NonNegativeInt] = None

    def to_db_box(self) -> DetectedBox:
        db_box = DetectedBox()

        db_box.top_x = self.top_x
        db_box.top_y = self.top_y
        db_box.bot_x = self.bot_x
        db_box.bot_y = self.bot_y

        db_box.detected_user = self.detected_user

        return db_box


class IFrameBoxes:
    boxes: list[IBox]


    class Config:

        json_encoders = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }

        json_decoders = {
            datetime: transform_to_utc_datetime
        }