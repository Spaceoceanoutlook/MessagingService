from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from .jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from messagingservice.models import User


def set_access_token(response: RedirectResponse, username: str):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
