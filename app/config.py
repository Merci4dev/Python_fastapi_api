
from pydantic import BaseSettings

# to provide the variable env the we need to set
class Settings(BaseSettings):
    database_hostname : str
    database_port : str
    database_password : str 
    database_name : str
    database_username : str
    secret_key : str 
    algorithm: str
    access_token_expire_minutes: int


    #impotando los valores del file .env
    class Config:
        env_file = ".env"

settings = Settings()