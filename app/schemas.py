from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class Index(BaseModel):
    Documentation: dict


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(Post):
    pass


class UpdatePost(Post):
    pass


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime


    class Config:
        orm_mode = True


class PostResponse(Post):
    id: int
    created_at: datetime
    user_id: int 
    user: UserResponse

    class Config:
        orm_mode = True


class User(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: int

