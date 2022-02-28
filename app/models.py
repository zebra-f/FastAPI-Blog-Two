from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    # AUTO
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    # JSON BODY
    title = Column(String, nullable=False)
    content= Column(String, nullable=False)
    # OTIONAL JSON BODY
    published = Column(Boolean, server_default='TRUE', nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User")


class User(Base):
    __tablename__ = "users"

    # AUTO
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    # JSON BODY
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)


class Vote(Base):
    __tablename__ = 'votes'

    # AUTO
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)


class Comment(Base):
    __tablename__ = 'comments'

    #AUTO
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False)

    #JSON BODY
    content = Column(String, nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    # post = relationship("Post")
    user = relationship("User")





