from starlette import status
from starlette.testclient import TestClient


def test_get_me(client: TestClient) -> None:
    reg_response = client.post(
        "/register", json={"email": "test4@email.ru", "role": "patient"}
    )
    response = client.get("/me", cookies={"token": reg_response.cookies.get("token")})

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["role"] == "patient"
