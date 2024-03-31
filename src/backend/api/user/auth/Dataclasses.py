import attrs


@attrs.define
class AuthLoginData:
    username: str
    password: str


@attrs.define
class AuthLoginResponse:
    token: str
    exp: str
