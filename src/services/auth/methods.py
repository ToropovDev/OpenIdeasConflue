from fastapi import APIRouter
import requests
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import OPEN_IDEAS_URL, OPEN_IDEAS_PROTECTED_ENDPOINT

security = HTTPBearer()


def verify_token_with_partner(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(
        f"{OPEN_IDEAS_URL}{OPEN_IDEAS_PROTECTED_ENDPOINT}", headers=headers
    )

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Token is invalid or expired")
    else:
        raise HTTPException(
            status_code=500, detail="Unable to verify token with partner"
        )


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
def login(email: str, password: str):
    response = requests.post(
        f"{OPEN_IDEAS_URL}/auth/password/", json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.json())


@router.post("/register")
def register(email: str, password: str):
    response = requests.post(
        f"{OPEN_IDEAS_URL}/auth/passreg/", json={"email": email, "password": password}
    )
    if response.status_code == 200:
        return response.json()
    raise HTTPException(status_code=response.status_code, detail=response.json())
