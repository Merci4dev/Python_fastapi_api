# USERS COMPONENT

# 1 invocacion de fastapi y methodos adicionales
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
# Importing the model and DB Engine, utils file
from .. import models, schema, utils
from .. database import get_db


router = APIRouter(
    # estableciendo el prefijo a la rutas
    prefix="/users",

    tags=["Users"]
)


# funcion to crate an user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOuth)
def create_user( user: schema.UserCreate, db: Session = Depends(get_db)):

    # Antes de crear un user creamos la passwd cifrada que se almacenara en la DB
    hashed_passwd = utils.pwd_hash(user.password)
    user.password = hashed_passwd

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user



# para manejar informaciones especificas sobre un user
@router.get("/{id}", response_model=schema.UserOuth)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    # validation
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User id Ivalid")
    
    return user