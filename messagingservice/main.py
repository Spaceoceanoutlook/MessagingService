import uvicorn
from fastapi import FastAPI
from messagingservice.api_v1.users.crud import router as users_router

app = FastAPI()
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
