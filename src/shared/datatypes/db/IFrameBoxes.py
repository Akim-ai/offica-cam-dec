from datetime import datetime

from pydantic import BaseModel, NonNegativeInt

from src.shared.datatypes.CustomFields.HexBytes import HexBytes
from src.shared.datatypes.db.IBox import IBox
from src.shared.datatypes.db.IFrame import IFrame
from src.shared.datatypes.json_encoders_decoders.datetime import convert_datetime_to_iso_8601_with_z_suffix, \
    transform_to_utc_datetime


class IFrameWithBoxes(BaseModel):
    frame: IFrame
    boxes: list[IBox]

    class Config:
        json_encoders = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }

        json_decoders = {
            datetime: transform_to_utc_datetime,
            HexBytes: bytes.fromhex,
        }
