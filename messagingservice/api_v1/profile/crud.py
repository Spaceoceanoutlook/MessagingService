import jwt
from fastapi import HTTPException, status, APIRouter, Request, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from messagingservice.api_v1.auth.utils_jwt import decode_jwt, set_access_token


router = APIRouter(tags=["Profile"])
templates = Jinja2Templates(directory="messagingservice/templates")


@router.get("/", response_class=HTMLResponse, summary="Главная страница")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/profile", response_class=HTMLResponse, summary="Профиль пользователя")
def get_index(
    request: Request,
    access_token: str = Cookie(None),
    refresh_token: str = Cookie(None),
):
    if access_token is None:
        return templates.TemplateResponse(
            "profile.html", {"request": request, "username": "ты кто?"}
        )
    try:
        user_data = decode_jwt(access_token)
        username = user_data.get("username")
    except jwt.ExpiredSignatureError:
        if refresh_token is None:
            return templates.TemplateResponse(
                "profile.html", {"request": request, "username": "ты кто?"}
            )
        try:
            refresh_data = decode_jwt(refresh_token)
            username = refresh_data.get("username")
            response = RedirectResponse(
                url="/profile", status_code=status.HTTP_302_FOUND
            )
            set_access_token(response, username)
            return response
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Refresh token expired"
            )
        except Exception as e:
            print(f"Error decoding refresh token: {e}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid refresh token"
            )

    return templates.TemplateResponse(
        "profile.html", {"request": request, "username": username}
    )
