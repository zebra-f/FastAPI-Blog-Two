from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_TEST_DATABASE_URL = "postgresql://test_user:1234@localhost/fastapi_blog_two_test"
# SQLALCHEMY_TEST_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db_testing():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()