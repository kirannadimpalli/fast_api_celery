from fastapi import FastAPI
from celery_project.users import users_router                # new


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(users_router) 

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app