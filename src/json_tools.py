import decimal
from typing import Any
from uuid import UUID

import orjson
from asyncpg.pgproto.pgproto import UUID as PG_UUID

DecodeError = orjson.JSONDecodeError
EncodeError = orjson.JSONEncodeError


def _default(obj: Any) -> str:
    match obj:
        case UUID() | PG_UUID():
            return str(obj)
        case decimal.Decimal():
            return str(obj)
        case _:
            raise NotImplementedError


def byte_encoder(obj: Any, option: int = 0) -> bytes:
    return orjson.dumps(
        obj,
        option=orjson.OPT_NAIVE_UTC | orjson.OPT_NON_STR_KEYS | option,
        default=_default,
    )


def encoder(obj: Any, option: int = 0) -> str:
    return byte_encoder(obj, option).decode()


def decoder(obj: str | bytes) -> Any:
    return orjson.loads(obj)
