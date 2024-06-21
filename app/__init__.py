from fastapi import FastAPI
from app.users import users_router                
from app.celery_utils import create_celery             


def create_app() -> FastAPI:
    app = FastAPI()

    # do this before loading routes             
    app.celery_app = create_celery()

    app.include_router(users_router) 

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app