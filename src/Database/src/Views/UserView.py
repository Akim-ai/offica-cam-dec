from faststream.rabbit import RabbitBroker

from src.Database.src.DBControllers.DBUserController import DBUserController
from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.db_data_queues import (
    queue_get_all_detected_users,
    queue_create_user, queue_get_user, queue_get_users, queue_delete_user, queue_get_auth_user
)
from src.shared.datatypes.api.Pagination import PaginatorPage
from src.shared.datatypes.api.UserViewType import AuthLoginData
from src.shared.datatypes.db.IUser import IUserWithImage, IListUserWithImage

UserController = DBUserController()


async def get_all_detected_users(msg: str = ''):
    return await UserController.get_all_detected_users()


async def get_user(msg: int) -> dict:
    return await UserController.get_user(user_id=msg)


async def create_detected_user(msg: dict) -> dict:
    data = IUserWithImage.model_validate(msg, from_attributes=True)
    return await UserController.create_user(data=data)


async def get_users(msg: PaginatorPage) -> dict:
    return await UserController.get_paginated_user(page=msg.page)


async def delete_user(msg: int) -> int:
    return await UserController.delete_user(user_id=msg)


async def get_auth_user(msg: AuthLoginData):
    return await UserController.get_auth_user(data=msg)

async def init_controller():
    await UserController.async_init()


async def create_user_annotations(_broker: RabbitBroker):
    await init_controller()
    _broker.subscriber(queue=queue_get_all_detected_users, exchange=exch)(get_all_detected_users)
    _broker.subscriber(queue=queue_get_user, exchange=exch)(get_user)
    _broker.subscriber(queue=queue_get_users, exchange=exch)(get_users)
    _broker.subscriber(queue=queue_create_user, exchange=exch)(create_detected_user)
    _broker.subscriber(queue=queue_delete_user, exchange=exch)(delete_user)
    _broker.subscriber(queue=queue_get_auth_user, exchange=exch)(get_auth_user)
