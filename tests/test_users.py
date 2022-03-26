from app import schemas


def test_create_user(client):
    email = "test_user_10@fastapi.com"
    password = "test_password"
    
    response = client.post("/users/", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 201

    new_user = schemas.UserResponse(**response.json())

    assert new_user.email == email


def test_login_user(client, test_user):
    email = test_user['email']
    password = test_user['password']
    
    response = client.post("/login/", data={
        "username": email,
        "password": password
    })

    login_response = schemas.TokenResponse(**response.json())
    
    assert login_response.token_type == "bearer"

    assert response.status_code == 202


