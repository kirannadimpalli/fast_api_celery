import requests
from unittest import mock
from app.users.models import User
from app.users import users_router


def test_pytest_setup(client, db_session):
    # test view
    response = client.get(users_router.url_path_for('form_example_get'))
    assert response.status_code == 200

    # test db
    user = User(username="test", email="test@example.com")
    with db_session.begin():
        db_session.add(user)
    assert user.id


def test_view_with_eager_mode(client, db_session, settings, monkeypatch):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    monkeypatch.setattr(settings, "CELERY_TASK_ALWAYS_EAGER", True, raising=False)

    user_name = "michaelyin"
    user_email = f"{user_name}@accordbox.com"
    response = client.post(
        users_router.url_path_for('user_subscribe'),
        json={"email": user_email, "username": user_name},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "send task to Celery successfully",
    }

    mock_requests_post.assert_called_with(
        "https://httpbin.org/delay/5",
        data={"email": user_email}
    )