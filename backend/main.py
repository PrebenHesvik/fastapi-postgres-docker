from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import todo_lists
from .models import __beanie_models__
from .database import init_db

app = FastAPI(
    title="Task List API", description="This is a simple API for a Task service"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(todo_lists.router)


@app.on_event("startup")
async def connect():
    await init_db()
    return {"message": "Todo app"}


# @app.get("/")
# def root():
#     return {"message": "Todo app"}
