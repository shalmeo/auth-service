from starlette import status
from starlette.testclient import TestClient


def test_register_user(client: TestClient) -> None:
    response = client.post(
        "/register", json={"email": "test@email.ru", "role": "patient"}
    )

    assert response.cookies.get("token") is not None
    assert response.status_code == status.HTTP_200_OK


def test_login_user(client: TestClient) -> None:
    client.post("/register", json={"email": "test1@email.ru", "role": "patient"})
    response = client.post("/login", json={"email": "test@email.ru"})

    assert response.cookies.get("token") is not None
    assert response.status_code == status.HTTP_200_OK


def test_login_non_existens_user(client: TestClient) -> None:
    response = client.post("/login", json={"email": "test2@email.ru"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
