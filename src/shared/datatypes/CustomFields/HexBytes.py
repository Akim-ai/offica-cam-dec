from typing import Any, Annotated

from pydantic import errors, PlainValidator, PlainSerializer


def hex_bytes_validator(val: Any) -> bytes:
    if isinstance(val, bytes):
        return val
    elif isinstance(val, bytearray):
        return bytes(val)
    elif isinstance(val, str):
        return bytes.fromhex(val)
    raise errors.BytesError()


def hex_bytes_serializer(val: Any) -> str:
    if isinstance(val, bytes):
        return val.hex()
    elif isinstance(val, bytearray):
        return val.hex()
    elif isinstance(val, str):
        return val


HexBytes = Annotated[bytes, PlainValidator(hex_bytes_validator), PlainSerializer(hex_bytes_serializer)]

