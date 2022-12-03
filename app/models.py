# each model represent a table in the database. Esto seria la estructura del un ORM

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

# model to create the posts
class Post(Base):
    __tablename__ = "posts"

    # definiendo las columnas en nuestra tabla de Post
    id = Column(Integer, primary_key=True, nullable=False) 

    title = Column(String,  nullable=False) 

    content = Column(String,  nullable=False) 

    published = Column(Boolean, server_default="TRUE",  nullable=False) 

    created_at = Column(TIMESTAMP(timezone=True), 
            nullable=False,  server_default=text(' now() ')) 

    # Crea la relacion entre las tablas
    owner_id = Column(Integer, ForeignKey(
    "users.id", ondelete="CASCADE"), nullable=False)

    # Crea una propiedad owner y establece la relacion para indentificar el nombre de quien crea el pos 
    owner = relationship("Users")


# Model class for the users
class Users(Base):
    __tablename__ = "users"

    # definiendo las columnas en nuestra tabla de users
    id = Column(Integer, primary_key=True, nullable=False) 

    email = Column(String, nullable=False, unique=True)

    password = Column(String, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), 
            nullable=False,  server_default=text(' now() ')) 

    phone_number = Column(String)


# Clase que maneja el modelo de los votos
class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)

    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)


