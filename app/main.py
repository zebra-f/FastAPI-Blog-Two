from fastapi import FastAPI
from typing import List
from sqlalchemy.orm import Session

from .database import engine
from . import models
from .routers import post, user, login


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Blog-One"
    )

app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)