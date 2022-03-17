from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import database, schemas
from .routers import post, user, login, vote, comment


database.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Blog-One"
    )


# Permissions for cross-origin requests.
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(login.router)
app.include_router(vote.router)
app.include_router(comment.router)


@app.get("/", response_model=schemas.Index, status_code=status.HTTP_200_OK)
def get_index():
    
    return {"Documentation": {"Swagger UI": "http://127.0.0.1:8000/docs",
                                "ReDoc": "http://127.0.0.1:8000/redoc"}}