# FILE maneja todo lo que tiene que ver con jwt
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schema, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import  Session
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl = 'login')


# Secret Key
SECRET_KEY = settings.secret_key

# Algoritmo to use
ALGORITHM = settings.algorithm

# Espiration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data : dict):
    to_encode = data.copy()

    # establece el tiempos de expiracion
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 

    return encoded_jwt


# Funcion para verificar el access token
def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schema.TokenData(id = id)

    except JWTError:
        raise credentials_exception
    
    return token_data


# funtion to  get the current user fron the DB
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(database.get_db)):

    credentials_exception  = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f'Could not Validate credentials', 
        headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user