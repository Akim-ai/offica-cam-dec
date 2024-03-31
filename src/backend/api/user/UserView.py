from datetime import datetime
import time

from faststream.rabbit import RabbitBroker
from sanic import json, Request, Sanic, HTTPResponse
from sanic.response import JSONResponse
from sanic_ext import validate

from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.db_data_queues import queue_create_user, queue_get_user, queue_get_users, \
    queue_delete_user, queue_get_frames_by_user
from src.shared.datatypes.api.FrameViewTypes import StartTimeByUser, StartTimeIn
from src.shared.datatypes.api.Pagination import PaginatorPage
from src.shared.datatypes.db.IUser import IUserWithImage


# @protected()
async def get_user(request: Request, user_id: int):
    app = Sanic.get_app()
    broker: RabbitBroker = app.ctx.broker
    print('before send')
    user = await broker.publish(message=user_id, queue=queue_get_user, exchange=exch, rpc=True)
    return json(user, status=200)


async def get_list_users(request: Request):
    print(request.args)
    page = request.args.get('page')
    if not page:
        page = 1
    body = PaginatorPage(page=page)
    print(page)
    app = Sanic.get_app()
    broker: RabbitBroker = app.ctx.broker
    print('before send')
    user = await broker.publish(message=body, queue=queue_get_users, exchange=exch, rpc=True)
    return json(user, status=200)


async def create_user(request: Request):
    start = time.perf_counter()
    user = IUserWithImage.model_validate_json(request.body)
    app = Sanic.get_app()
    broker: RabbitBroker = app.ctx.broker
    print('before send')
    user = await broker.publish(message=user.model_dump_json(), queue=queue_create_user, exchange=exch, rpc=True)
    print(user)
    print(time.perf_counter() - start)
    return json({"data": user}, status=201)


async def delete_user(request: Request, user_id: int):
    if user_id < 1:
        return json({'error': 'value must be positive'}, status=400)
    app = Sanic.get_app()
    broker: RabbitBroker = app.ctx.broker

    user_message = await broker.publish(message=user_id, queue=queue_delete_user, exchange=exch, rpc=True)
    return json({'deleted': user_id}, status=user_message)


async def get_frames_by_user(request: Request, user_id: int):
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

    message: StartTimeByUser = StartTimeByUser.model_validate({"user_id": user_id, **{"page": page, "start": start}}, from_attributes=True)
    paginated_frames = await broker.publish(message=message, queue=queue_get_frames_by_user, exchange=exch, rpc=True)
    return json(paginated_frames)
