import uvicorn
from fastapi import FastAPI
from messagingservice.api_v1.auth.crud import router as auth_router
from messagingservice.api_v1.chat.crud import router as profile_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(profile_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
