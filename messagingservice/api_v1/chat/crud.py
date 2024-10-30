from fastapi import HTTPException, status, APIRouter, Request, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(tags=["Profile"])
templates = Jinja2Templates(directory="templates")


@router.get("/",
            response_class=HTMLResponse,
            summary="Главная страница")
def root(request: Request):
    # return RedirectResponse(url="/auth/register")
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/profile",
            response_class=HTMLResponse,
            summary="Профиль пользователя")
def get_index(request: Request, access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")
    return templates.TemplateResponse("profile.html", {"request": request, "username": request.cookies.get("username")})
