
# commands

``` sh
uvicorn main:app --reload # to run fastAPI

notepad $PROFILE

. $PROFILE

celery -A app.main.celery worker -l info --pool=solo #NOTE windows pool is need for windows

celery -A app.main.celery flower --port=5555 #to check task status flower


alembic revision --autogenerate

```