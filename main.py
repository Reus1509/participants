from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers.user_router import router as user_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
