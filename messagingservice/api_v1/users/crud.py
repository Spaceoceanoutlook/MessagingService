from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from messagingservice import schemas, models, utils
from .jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from messagingservice.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register",
             response_model=schemas.UserResponse,
             summary="Регистрация пользователя",
             description="Регистрирует нового пользователя в базе данных")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    hashed_password = utils.hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return schemas.UserResponse(id=db_user.id, username=db_user.username, email=db_user.email)


@router.post("/login",
             summary="Аутентификация пользователя",
             description="В случае успешной аутентификации возвращает JWT-токен")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
