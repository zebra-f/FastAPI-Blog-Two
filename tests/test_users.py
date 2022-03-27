import pytest

from app import schemas


def test_create_user(client):
    email = "test_user_10@fastapi.com"
    password = "test_password_*47"
    
    response = client.post("/users/", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 201

    new_user = schemas.UserResponse(**response.json())

    assert new_user.email == email


@pytest.mark.parametrize('email, password, status_code', [
    (None, "test_password_*47", 422),
    ("test_user_11@fastapi", "test_password_*47", 422),
    ("test_user_12@fastapi.com", None, 422),
    
    ("test_user_14@fastapi.com", "test_password_*", 406),
    ("test_user_15@fastapi.com", "test_password", 406),
    ("test_user_16@fastapi.com", "testpassword47", 406),
    ("test_user_17@fastapi.com", "te_p_*47", 406),

    ("test_user_18@fastapi.com", "test_47", 406),
    ("test_user_19@fastapi.com", "test_password_47*" + ''.join(str(i) for i in range(4096)), 406)

])
def test_create_user_invalid(client, email, password, status_code):

    response = client.post('/users/', json= {
        "email": email,
        "password": password
    })

    assert response.status_code == status_code
