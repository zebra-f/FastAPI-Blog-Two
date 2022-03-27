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


