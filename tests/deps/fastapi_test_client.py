from fastapi.testclient import TestClient
from pytest import fixture
import pytest

from app.main import app
from app.database import Base, get_db
from .database_test_session import engine, TestingSessionLocal


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Dependency
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
    
