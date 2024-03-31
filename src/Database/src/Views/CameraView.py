from typing import Union

from faststream.rabbit import RabbitBroker

from src.shared.RabbitMQExchange import exch as exchange
from src.Database.src.DBControllers.DBCameraController import DBCameraController
from src.shared.RabbitMQQueues.db_data_queues import queue_create_camera, \
    queue_get_frame_processors, queue_get_all_data_gets, queue_get_camera, queue_get_cameras, queue_put_camera
from src.shared.datatypes.api.CameraViewTypes import IPutCamera
from src.shared.datatypes.api.Pagination import PaginatorPage
from src.shared.datatypes.db.ICamera import ICamera


CameraController = DBCameraController()


async def create_camera(msg: ICamera):
    if msg:
        return await CameraController.create_camera(data=msg)
    raise Exception("No data")


async def get_frame_processors(msg: str) -> str:
    return await CameraController.get_all_frame_processors()


async def get_all_data_gets(msg: str) -> str:
    return await CameraController.get_all_data_gets()


async def get_camera(msg: int) -> dict:
    return await CameraController.get_camera(camera_id=msg)


async def get_cameras(msg: PaginatorPage) -> dict:
    return await CameraController.get_cameras(page=msg.page)


async def put_camera(msg: ICamera):
    return await CameraController.put_camera(camera=msg)


async def init_controller():
    await CameraController.async_init()


async def create_camera_annotations(_broker: RabbitBroker):
    await init_controller()
    _broker.subscriber(queue=queue_create_camera, exchange=exchange)(create_camera)
    _broker.subscriber(queue=queue_get_camera, exchange=exchange)(get_camera)
    _broker.subscriber(queue=queue_get_cameras, exchange=exchange)(get_cameras)
    _broker.subscriber(queue=queue_put_camera, exchange=exchange)(put_camera)

    _broker.subscriber(queue=queue_get_frame_processors, exchange=exchange)(get_frame_processors)
    _broker.subscriber(queue=queue_get_all_data_gets, exchange=exchange)(get_all_data_gets)
