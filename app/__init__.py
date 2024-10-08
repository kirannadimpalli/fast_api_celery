from contextlib import asynccontextmanager
from broadcaster import Broadcast
from fastapi import FastAPI

from app.config import settings

broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    from app.users import users_router
    app.include_router(users_router)
    # do this before loading routes
    from app.celery_utils import create_celery
    app.celery_app = create_celery()

    from app.logging import configure_logging          # new
    configure_logging()                                    


    from app.ws import ws_router                   # new
    app.include_router(ws_router) 


    from app.ws.views import register_socketio_app         # new
    register_socketio_app(app)                                 # new

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app