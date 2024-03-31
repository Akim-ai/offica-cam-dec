from typing import Optional

from pydantic import BaseModel

from src.Database.Models import Camera


class ICamera(BaseModel):
    id: Optional[int] = None
    name: str
    ip_endpoint: str
    is_active: bool = True

    @staticmethod
    def __assign_fields(obj_to, obj_from):
        obj_to.name = obj_from.name
        obj_to.ip_endpoint = obj_from.ip_endpoint
        obj_to.is_active = obj_from.is_active

        return obj_to

    def to_db_camera(self) -> Camera:
        camera = Camera()
        camera = self.__assign_fields(obj_to=camera, obj_from=self)

        return camera


class ICameraList(BaseModel):
    cameras: list[ICamera] = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cameras = self.cameras if self.cameras else []
