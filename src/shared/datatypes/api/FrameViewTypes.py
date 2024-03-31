import datetime

from pydantic import BaseModel, NonNegativeInt

from src.shared.datatypes.json_encoders_decoders.datetime import convert_datetime_to_iso_8601_with_z_suffix, \
    transform_to_utc_datetime


class StartTime(BaseModel):
    start: datetime.datetime
    page: NonNegativeInt

    class Config:

        json_encoders = {
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }

        json_decoders = {
            datetime: transform_to_utc_datetime,
        }


class StartTimeIn(StartTime):
    camera_id: NonNegativeInt


class StartTimeByUser(StartTime):
    user_id: NonNegativeInt
