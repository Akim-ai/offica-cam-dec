from datetime import datetime
from faststream.rabbit import RabbitBroker
from sanic import Request, Sanic, json
from sanic_ext import validate

from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.db_data_queues import queue_get_frames
from src.shared.datatypes.api.FrameViewTypes import StartTime, StartTimeIn


async def get_frames(request: Request, camera_id: int):
    broker: RabbitBroker = Sanic.get_app().ctx.broker

    args = request.args
    start = args.get("start")
    if not start:
        return json({"error": "No {start} provided"})

    page = 1
    try:
        start = datetime.fromisoformat(start)

    except ValueError as e:
        if start[-1] == "Z":
            start = start[:-1]

    print(page, start)

    message: StartTimeIn = StartTimeIn.model_validate({'camera_id': camera_id, **{"page": page, "start": start}}, from_attributes=True)
    paginated_frames = await broker.publish(message=message, queue=queue_get_frames, exchange=exch, rpc=True)
    return json(paginated_frames)


