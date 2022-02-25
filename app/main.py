from fastapi import FastAPI, status
from sqlalchemy.orm import Session

from .database import engine
from . import models, schemas
from .routers import post, user, login, vote, comments


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Blog-One"
    )


app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(vote.router)
app.include_router(comments.router)


@app.get("/", response_model=schemas.Index, status_code=status.HTTP_200_OK)
def get_index():
    return {"Documentation": {"Swagger UI": "http://127.0.0.1:8000/docs",
                                "ReDoc": "http://127.0.0.1:8000/redoc"}}