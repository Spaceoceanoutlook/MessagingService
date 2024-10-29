from fastapi import Depends, HTTPException, status, APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from messagingservice import schemas, models, utils
from messagingservice.database import get_db
from .jwt import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/users", tags=["Users"])
templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register",
             response_model=schemas.UserResponse,
             summary="Регистрация пользователя",
             description="Регистрирует нового пользователя в базе данных")
def register(username: str = Form(...), email: str = Form(...), password: str = Form(...),
             db: Session = Depends(get_db)):
    user = schemas.UserCreate(username=username, email=email, password=password)
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    hashed_password = utils.hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return RedirectResponse(url="/users/login", status_code=status.HTTP_302_FOUND)


@router.get("/login", response_class=HTMLResponse)
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login",
             summary="Аутентификация пользователя",
             description="В случае успешной аутентификации возвращает JWT-токен")
def login(username: str = Form(...), password: str = Form(...),
          db: Session = Depends(get_db)):
    user = schemas.UserAuth(username=username, password=password)
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": db_user.username},
                                       expires_delta=access_token_expires)
    # Редирект на страницу /index после успешной аутентификации
    response = RedirectResponse(url="/index", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=access_token, httponly=True)  # Устанавливаем токен в cookie
    return response
