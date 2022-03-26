from app import schemas


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


def test_login_user_incorrect_pass(test_user, client):
    email = test_user['email']
    password = 'incorrect_password'
    
    response = client.post("/login/", data={
        "username": email,
        "password": password
    })

    assert response.status_code == 403
    assert response.json().get('detail') == 'Invalid credentials'


def test_login_user_incorrect_email(client, test_user):
    email = 'incorrect_email'
    password = test_user['password']
    
    response = client.post("/login/", data={
        "username": email,
        "password": password
    })

    assert response.status_code == 403
    assert response.json()['detail'] == 'Invalid credentials'