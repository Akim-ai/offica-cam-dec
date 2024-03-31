from typing import Optional, Any

from pydantic import BaseModel, NonNegativeInt
from datetime import datetime

from src.Database.Models import Frame
from src.shared.datatypes.CustomFields.HexBytes import HexBytes
from src.shared.datatypes.json_encoders_decoders.datetime import \
    convert_datetime_to_iso_8601_with_z_suffix, transform_to_utc_datetime


class IFrame(BaseModel):
    id: Optional[NonNegativeInt] = 0
    camera: NonNegativeInt
    boxes: list[int] = []
    path: str = ''
    created_at: datetime

    frame: HexBytes

    class Config:

        json_encoders = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }

        json_decoders = {
            datetime: transform_to_utc_datetime,
            HexBytes: bytes.fromhex,
        }

    def __init__(self, camera: NonNegativeInt | int, created_at: datetime, path: str = '', frame: HexBytes = None,
                 **data: Any):
        super().__init__(camera=camera, created_at=created_at, path=path, frame=frame)
        self.camera = camera
        self.frame = frame
        self.path = path
        self.created_at = created_at

    def to_db_frame(self) -> Frame:
        frame: Frame = Frame()
        frame.camera = self.camera
        frame.frame = self.path
        frame.created_at = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        return frame

    @classmethod
    async def from_db_frame(cls, frame: Frame) -> 'IFrame':
        i_frame = IFrame(
            id=frame.id, camera=frame.camera,
            boxes=frame.boxes, path=frame.frame,
            created_at=frame.created_at
        )
        return i_frame



