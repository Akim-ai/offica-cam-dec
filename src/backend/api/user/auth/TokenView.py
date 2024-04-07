from typing import Optional
from uuid import UUID

import jwt

from faststream.rabbit import RabbitBroker
from sanic import HTTPResponse, text, Request, json, Sanic
from sanic_ext import validate
from sqlalchemy import select, Result

from src.shared.RabbitMQExchange import exch
from src.shared.RabbitMQQueues.db_data_queues import queue_get_auth_user
from src.shared.datatypes.api.UserViewType import AuthLoginData


async def login_token(request: Request, **kwargs):
    body = AuthLoginData.model_validate_json(request.body)
    app = Sanic.get_app()
    broker: RabbitBroker = app.ctx.broker

    
    result: dict = await broker.publish(message=body.model_dump(), queue=queue_get_auth_user, exchange=exch, rpc=True, rpc_timeout=3)
    
    if result.get("error"):
        return json(result, status=401)
    print(result)
    result = jwt.encode(result, app.config["secret"], app.config["jwt_alg"])

    print(f'{body=}\n{result=}')
    return json(result)


async def refresh_token(request):
    """

    :param request:
    :return:
    """
    return text('REFRESH TOKEN')

