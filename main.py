from celery import Celery
from app import create_app
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()



app = create_app()
celery = app.celery_app

celery = Celery(
    __name__,
    broker=os.getenv("BROKER"),
    backend=os.getenv("BACKEND")
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y