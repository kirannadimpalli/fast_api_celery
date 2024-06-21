from celery import Celery
from fastapi import FastAPI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()



app = FastAPI()

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