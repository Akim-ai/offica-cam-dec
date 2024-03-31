import datetime

from pydantic import BaseModel, Field, EncodedBytes, NonNegativeInt


class NotProcessedImage:
    image: bytes
    cam_id: int
    time: datetime.datetime



