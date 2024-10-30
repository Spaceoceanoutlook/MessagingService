from fastapi import HTTPException, status, APIRouter, Request, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(tags=["Profile"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=RedirectResponse)
def root():
    return RedirectResponse(url="/auth/register")


@router.get("/profile", response_class=HTMLResponse)
def get_index(request: Request, access_token: str = Cookie(None)):
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated")

    # Здесь вы можете добавить логику для проверки токена
    # Например, декодировать токен и проверить его валидность

    return templates.TemplateResponse("profile.html", {"request": request})
