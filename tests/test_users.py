from app.main import client
from app.utilities import b_pass
from app import schemas


def test_create_user():
    email = "tests_user4@email.com"
    password = b_pass.get_password_hash("tests_password")
    
    response = client.post("/users/", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 201

    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == email

    