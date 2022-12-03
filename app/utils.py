# Este file amacena utilidades de la app (como el cifrado de la passwd)

from passlib.context import CryptContext
#Definiendo el tipo de encrptado que usaremos
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def pwd_hash(password: str):
    return pwd_context.hash(password)


# Funtion to compare the hashes
def veriry(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)