# This file handle the database connection and the ORM
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Driver to connect python with postgres
import psycopg2
from psycopg2.extras import RealDictCursor
#13 Modu time 
import time
from .config import settings

# Url which reference the database (for the connection)
# SQLALCHEMY_DATABASE_URL = "postgresql://merci4dev:elnobato007@localhost/fastapidb"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


# The engine is responsable to connect the ORM(sqlalchemy) to postgres
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency for the section
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




