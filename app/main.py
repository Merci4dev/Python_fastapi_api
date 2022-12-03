
# 1 invocacion de fastapi y methodos adicionales
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importing the model and DB Engine, utils file
from . import models
from .database import engine
# importacion de la rutas
from .routes import posts, users, auth, votes
from .config import settings

# this line crate the table
# models.Base.metadata.create_all(bind=engine)

#2 Instanciacion de fastapi
app = FastAPI()

# for all kind of domain(public)
origins = ["*"]

# for especific kind of domain(public)
# origins = [
#     "https://tudomini.com",
#     "https://demo.com",
    
#     ]

#  thid middleware se ejecuta antes de haceder a las rutas. Aqui especificamos los rigenes permitidos
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Usando las rutas que apunta a users como a posts
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


# 3 GET: Function which render the home page 
@app.get("/")  
def root():
    return {"message": "Wellcome to my HOme Page App"}



# fetch("http://127.0.0.1:8000").then(resp => resp.json()).then(data => console.log(data))
# fetch("https://locahost:8000").then(resp => resp.json()).then(data => console.log(data))

# fetch('http://localhost:8000').then(res => res.json()).then(console.log)