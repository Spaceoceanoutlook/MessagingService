import jwt
from config import settings
from fastapi.responses import RedirectResponse
from datetime import datetime, timezone, timedelta


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.auth_jwt.access_token_expire_minutes
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
    access_token = encode_jwt(payload={"username": username})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response
