from pydantic import BaseModel, field_validator


class AuthLoginData(BaseModel):
    username: str
    password: str

    # @field_validator('username')
    # @classmethod
    # def validate_len_username(cls, v: str):
    #     if len(v) > 50:
    #         raise ValueError('username is too length')
    #
    # @field_validator('password')
    # @classmethod
    # def validate_len_username(cls, v: str):
    #     if len(v) > 50:
    #         raise ValueError('password is too length')
