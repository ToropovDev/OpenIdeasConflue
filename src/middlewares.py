import typing as t
import requests
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import OPEN_IDEAS_URL, OPEN_IDEAS_PROTECTED_ENDPOINT
from fastapi import Request
from fastapi import Response

security = HTTPBearer()


async def auth(
    request: Request,
    call_next: t.Callable[[Request], t.Awaitable[Response]],
) -> Response:
    token = request.headers.get('Authorization')
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{OPEN_IDEAS_URL}{OPEN_IDEAS_PROTECTED_ENDPOINT}", headers=request.headers
    )

    if response.status_code == 200:
        return await call_next(request)
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")
    else:
        raise HTTPException(
            status_code=500, detail="Unable to verify token with partner"
        )
