from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from .database_test_session import engine, override_get_db


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

Base.metadata.create_all(bind=engine)
