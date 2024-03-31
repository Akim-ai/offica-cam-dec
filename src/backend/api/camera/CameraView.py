from faststream.rabbit import RabbitBroker
from sanic import json, Sanic, HTTPResponse, Request
from sanic_ext import validate

from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.db_data_queues import queue_create_camera, queue_get_camera, queue_get_cameras, \
    queue_put_camera
from src.shared.datatypes.api.CameraViewTypes import IPutCamera, IPostCamera
from src.shared.datatypes.api.Pagination import PaginatorPage


@validate(IPostCamera)
async def create_camera(request: Request, body: IPostCamera) -> HTTPResponse:
    app = Sanic.get_app()
    broker: RabbitBroker = app.ctx.broker

    camera = await broker.publish(message=body, queue=queue_create_camera, exchange=exch, rpc=True)
    return json({"camera": camera})


async def get_camera(request: Request, camera_id: int) -> HTTPResponse:
    broker: RabbitBroker = Sanic.get_app().ctx.broker
    camera = await broker.publish(message=camera_id, queue=queue_get_camera, exchange=exch, rpc=True)
    return json(camera)


async def get_cameras(request: Request) -> HTTPResponse:
    page = request.args.get("page")
    print(page)
    if page:
        page = page[0]
    broker: RabbitBroker = Sanic.get_app().ctx.broker
    paginated_camera = await broker.publish(message=PaginatorPage(page=page), queue=queue_get_cameras, exchange=exch, rpc=True)
    print(paginated_camera)
    return json(paginated_camera)


@validate(IPostCamera)
async def put_camera(request: Request, body: IPutCamera, camera_id: int = 0):
    broker: RabbitBroker = Sanic.get_app().ctx.broker
    if not body.id and not camera_id:
        return HTTPResponse(body='', status=500)
    elif not body.id and camera_id > 0:
        body.id = camera_id
    result = await broker.publish(message=body, queue=queue_put_camera, exchange=exch, rpc=True)
    return HTTPResponse(body=result)

