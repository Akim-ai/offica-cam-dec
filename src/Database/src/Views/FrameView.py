from datetime import datetime, timezone

from faststream.rabbit import RabbitBroker

from src.Database.src.DBControllers.DBFrameController import DBFrameController
from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.db_data_queues import queue_create_frame, \
    queue_create_frame_with_boxes, queue_get_frames, queue_get_frames_by_user
from src.shared.datatypes.api.FrameViewTypes import StartTime, StartTimeIn, StartTimeByUser
from src.shared.datatypes.db import IFrameWithBoxes
from src.shared.datatypes.db.IFrame import IFrame

FrameController = DBFrameController()


async def create_frame(msg: str):
    data = IFrame.model_validate_json(msg)
    data.frame = bytes.fromhex(data.frame)
    data.created_at = datetime.fromisoformat(data.created_at).astimezone(tz=timezone.utc)
    frame = await FrameController.create_frame(data)
    return frame


async def create_frame_with_boxes(msg: str):
    data = IFrameWithBoxes.model_validate_json(msg)
    data.frame.frame = bytes.fromhex(data.frame.frame)
    data.frame.created_at = datetime.fromisoformat(data.frame.created_at).astimezone(tz=timezone.utc)
    await FrameController.create_frame_with_boxes(data=data)


async def get_frames(msg: StartTimeIn):
    return await FrameController.get_frames(data=msg)


async def get_frames_by_user(msg: StartTimeByUser):
    return await FrameController.get_frames_by_user(data=msg)


async def init_controller():
    await FrameController.async_init()



async def create_frame_annotations(_broker: RabbitBroker):
    await init_controller()
    _broker.subscriber(queue=queue_create_frame, exchange=exch)(create_frame)
    _broker.subscriber(queue=queue_create_frame_with_boxes, exchange=exch)(create_frame_with_boxes)
    _broker.subscriber(queue=queue_get_frames, exchange=exch)(get_frames)
    _broker.subscriber(queue=queue_get_frames_by_user, exchange=exch)(get_frames_by_user)

