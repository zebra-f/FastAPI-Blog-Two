from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app
from app.database import Base, get_db
from .deps.database_test_session import engine, TestingSessionLocal


@fixture(scope="module")
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Dependency
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture(scope="module")
def client(session):
    def override_get_db():
            yield session
 
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    

@fixture
def test_user(client):
    email = "test_user_1@fastapi.com"
    password = "test_password"

    response = client.post("/users/", json={
        "email": email,
        "password": password
    })

    assert response.status_code == 201
    
    new_user = response.json()
    new_user['password'] = password

    return new_user
    
