from fastapi import HTTPException, status, APIRouter, Request, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from messagingservice.api_v1.auth.utils_jwt import decode_jwt

router = APIRouter(tags=["Profile"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, summary="Главная страница")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/profile", response_class=HTMLResponse, summary="Профиль пользователя")
def get_index(request: Request, access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
        )
    user_data = decode_jwt(access_token)
    username = user_data.get("username")
    return templates.TemplateResponse(
        "profile.html", {"request": request, "username": username}
    )
