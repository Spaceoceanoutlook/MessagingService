import os
from fastapi import HTTPException, status
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def set_access_token(response: RedirectResponse, username: str):
    access_token = create_access_token(data={"username": username})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


def verify_token(access_token: str):
    try:
        return jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
