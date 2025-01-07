import typing as t

from fastapi import Request
from fastapi import Response


async def auth(
    request: Request,
    call_next: t.Callable[[Request], t.Awaitable[Response]],
) -> Response:

    # TODO: handle auth here

    return await call_next(request)
