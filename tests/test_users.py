from tests.deps.fastapi_test_client import client
from app.utilities import b_pass
from app import schemas


def test_create_user(client):
    email = "test_user_1@email.com"
    password = b_pass.get_password_hash("tests_password")
    
    response = client.post("/users/", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 201

    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == email

    