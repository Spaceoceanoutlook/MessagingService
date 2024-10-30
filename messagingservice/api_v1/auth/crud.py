from fastapi import Depends, HTTPException, status, APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from messagingservice import schemas, models, utils
from messagingservice.database import get_db
from .service import get_user_by_username, set_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="templates")


@router.get("/register",
            response_class=HTMLResponse,
            summary="Форма HTML для регистрации")
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register",
             summary="Регистрация пользователя",
             description="Регистрирует нового пользователя в базе данных")
def register(username: str = Form(...), email: str = Form(...), password: str = Form(...),
             db: Session = Depends(get_db)):
    user = schemas.UserCreate(username=username, email=email, password=password)
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    hashed_password = utils.hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    response = RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)
    set_access_token(response, db_user.username)
    response.set_cookie(key="username", value=db_user.username)
    return response


@router.get("/login",
            response_class=HTMLResponse,
            summary="Форма HTML для аутентификации")
def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login",
             summary="Аутентификация пользователя",
             description="В случае успешной аутентификации возвращает JWT-токен")
def login(username: str = Form(...), password: str = Form(...),
          db: Session = Depends(get_db)):
    user = schemas.UserAuth(username=username, password=password)
    db_user = get_user_by_username(db, user.username)
    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    response = RedirectResponse(url="/profile", status_code=status.HTTP_302_FOUND)
    set_access_token(response, db_user.username)
    response.set_cookie(key="username", value=db_user.username)
    return response
