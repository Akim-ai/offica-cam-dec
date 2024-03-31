from typing import Optional
from uuid import UUID

from faststream.rabbit import RabbitBroker
from sanic import text, Request, json, Sanic
from sanic_ext import validate
from sqlalchemy import select, Result

from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.db_data_queues import queue_get_auth_user
from src.shared.datatypes.api.UserViewType import AuthLoginData


# @validate(json=AuthLoginData)
async def login_token(request: Request, **kwargs):
    body = AuthLoginData.model_validate_json(request.body)
    broker: RabbitBroker = Sanic.get_app().ctx.broker
    result: dict = {
        'token': await broker.publish(message=body, queue=queue_get_auth_user, exchange=exch, rpc=True, rpc_timeout=3)
    }
    print(f'{body=}\n{result=}')
    return json(result)


async def refresh_token(request):
    """

    :param request:
    :return:
    """
    return text('REFRESH TOKEN')

