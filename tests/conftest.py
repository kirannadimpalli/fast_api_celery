import os
import sys

import pytest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ["FASTAPI_CONFIG"] = "testing"  # noqa


@pytest.fixture
def settings():
    from app.config import settings as _settings
    return _settings


@pytest.fixture
def app(settings):
    from app import create_app

    app = create_app()
    return app


@pytest.fixture()
def db_session(app):
    from app.database import Base, engine, SessionLocal

    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(app):
    from fastapi.testclient import TestClient

    yield TestClient(app)