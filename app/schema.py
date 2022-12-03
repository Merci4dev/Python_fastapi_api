
#5 con la librefia pydantic estableceremos el esquema de los datos lo cual estaremos recibiendo de los users. Esto hace la validacion por nosotros. Esto se asegura de que cuando el suer esta creando un un post tenga los campos que emos definidos previamente

# Crearemos un modelo para cada una de las diferentes request
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


# Defininendo una clase la cual las demas clases pueden eredar. En esta definimos cuales datos requeriremos del user 
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# la clase CreatePost eredare del la clse padre PostBase
class PostCreate(PostBase):
   pass


# Con esto el user no puede proveer nuvos fields al momento de actualizar un post
#class UpdatePost(PostBase):
    #published: bool 

'''
#Asi esecificamos que queremos devolver al user
class Post(BaseModel):
    #id: int
    #id: int
    title: str
    #content: str
    created_at : datetime
'''

# Defining whid data we send back to the user. Con esto evitamos que la passwor se retorner
class UserOuth(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime

    class Config:
        orm_mode = True


#This class handle the filed which must be send basck als response whe we make any request
class Post(PostBase):
    #id: int
    id: int
    created_at : datetime
    owner_id : int
    owner : UserOuth

    class Config:
        orm_mode = True


# Schema for the JOIN
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True


# USER SECTION
class UserCreate(BaseModel):
    email : EmailStr
    password : str
   

# Esquema para el Login User
class UsserLogin(BaseModel):
    email : EmailStr
    password: str


# Estbleciendo un schema for the token
class Tocken(BaseModel):
    access_token : str
    token_type : str


# Estbleciendo un schema for the token data
class TokenData(BaseModel):
    id: Optional[str] = None


# Estbleciendo un schema for the votes
class Votes(BaseModel):
    post_id : int
    dir: conint(le=1)
