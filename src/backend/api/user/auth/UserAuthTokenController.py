import uuid
from datetime import datetime, timezone, timedelta
from functools import wraps

import jwt
from sanic import text, Request, json, Sanic
from sqlalchemy import select, Result

from src.Database.Main.DB import DBSession
from src.backend.api.user.auth.Dataclasses import AuthLoginData
from src.Database.Models.User import User


class AuthTokenCheckResult:
    no_token: str = 'No Token Provided'
    expired: str = 'Token expired'
    invalid: str = 'Token invalid'
    correct: str = ''


class UserAuthTokenController:

    @staticmethod
    def __get_token_secret(request: Request):
        env = Sanic.get_app().ctx.env
        secret = env('SERVER_SECRET_TOKEN')
        return secret + request.client_ip

    @staticmethod
    async def create_token(request: Request, user_id: int):
        env = Sanic.get_app().ctx.env
        token = jwt.encode(
            {
                "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=env('JWT_ACCESS_TOKEN_EXP_TIME')),
                "user_id": user_id
            },
            UserAuthTokenController.__get_token_secret(request=request),
            algorithm="HS256"
        )
        print(token)
        return token

    @staticmethod
    async def check_token(request: Request) -> str:
        check_result = AuthTokenCheckResult()
        user: User
        auth_token: str = request.headers.get('Authorization')
        if not auth_token:
            return check_result.no_token
        try:
            decoded = jwt.decode(
                auth_token, UserAuthTokenController().__get_token_secret(request=request), algorithms=["HS256"]
            )

        except jwt.exceptions.ExpiredSignatureError:
            return check_result.expired
        except jwt.exceptions.InvalidTokenError:
            return check_result.invalid
        print(decoded)
        return check_result.correct


def protected(get_user: bool = False):
    def wrapper(wrapped):
        def decorator(f: callable):

            @wraps(f)
            async def decorated_function(request: Request, *args, **kwargs):
                token_code = await UserAuthTokenController.check_token(request)
                if token_code:
                    return text(body=token_code, status=200)
                response = await f(request, *args, **kwargs)
                return response

            return decorated_function

        return decorator(wrapped)

    return wrapper
