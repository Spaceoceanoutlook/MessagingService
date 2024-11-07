import jwt
from config import settings
from fastapi.responses import RedirectResponse
from datetime import datetime, timezone, timedelta


def encode_access_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    to_encode = payload.copy()
    to_encode.update({"type": "access"})
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.auth_jwt.access_token_expire_minutes
    )
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def encode_refresh_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    to_encode = payload.copy()
    to_encode.update({"type": "refresh"})
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.auth_jwt.refresh_token_expire_days
    )
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def set_access_token(response: RedirectResponse, username: str):
    access_token = encode_access_jwt(payload={"username": username})
    response.set_cookie(
        key="access_token", value=access_token, httponly=True, secure=True
    )
    return response


def set_refresh_token(response: RedirectResponse, username: str):
    refresh_token = encode_refresh_jwt(payload={"username": username})
    response.set_cookie(
        key="refresh_token", value=refresh_token, httponly=True, secure=True
    )
    return response
