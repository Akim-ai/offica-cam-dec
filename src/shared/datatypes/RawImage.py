from datetime import datetime, timezone

from pydantic import BaseModel

from src.shared.datatypes.CustomFields.HexBytes import HexBytes
from src.shared.datatypes.json_encoders_decoders.datetime import \
    convert_datetime_to_iso_8601_with_z_suffix, transform_to_utc_datetime


class RawImage(BaseModel):
    image: HexBytes
    time: datetime = datetime.now()

    def __init__(self, image: HexBytes, time: datetime = None):
        if not time:
            time = datetime.now().astimezone(timezone.utc)
            print(f"{time=}")
        super().__init__(image=image, time=time)
        self.image = image
        self.time = time

    class Config:
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601_with_z_suffix
        }
        json_decoders = {
            datetime: transform_to_utc_datetime
        }
