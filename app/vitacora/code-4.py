# 1 invocacion de fastapi y methodos adicionales
from fastapi import FastAPI, Response, status, HTTPException, Depends
#5 Para definir el modelo de los datos
from pydantic import BaseModel
from typing import Optional
# para establecer un id rando
from random import randrange
# Driver to connect python with postgres
import psycopg2
from psycopg2.extras import RealDictCursor
#13 Modu time 
import time

from sqlalchemy.orm import Session

# Importing the model and DB Engine
from . import models
from .database import engine, get_db

# this line crate the table
models.Base.metadata.create_all(bind=engine)
#2 Instanciacion de fastapi
app = FastAPI()


#12 conexion a la DB
# Comando para conectarse desde la db (uvicorn app.main:app --reload --port 5000)
while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapidb", user="merci4dev", password="elnobato007", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB is connectd succesfully...")
        break
    
    except Exception as error:
            print("Connection to DB failed")
            print("Error: ", error)
            #13 Si la conecion fall cada 2 intentara reconectarse nuenuevo
            time.sleep(2)
    


#5 con la librefia pydantic estableceremos el esquema de los datos lo cual estaremos recibiendo de los users. Esto hace la validacion por nosotros
# title str, content str, category, datetime Boll, etc
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating_p: Optional[int] = None # opcional field


# 6 variable global par guardar los posts de forma estatica
my_posts = [
    { 
    "title": "Post title No1",
    "content": "Post content No1",
    "id": 1,
  },
    { 
    "title": "Post title No2",
    "content": "Quiero aprender a programar rapido",
    "id": 2,
  },
    { 
    "title": "Post title No3",
    "content": "Me gustaria aprender a cocinar",
    "id": 3,
  },

] 


# 9 funcion para encontrar un post por su id
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


#10 funcion que en cuentra el indice de un post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
        print(i)


# 3 GET: Function which render the home page 
@app.get("/")  
def root():
    return {"message": "Wellcome to my HOme Page App"}



# GET: Get all post function
@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):

    #  make connection with the the DB thow the model ang get all post
    posts = db.query(models.Post).all()
    return {'data': posts}


# CREATE: Create post function
# status_code=status.HTTP_201_CREATED (permite cambiar el stado del codigo arrojado)
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):


    # si el formulario cuenta de mucho imputs(title, name etc...) lo mas viable es uar un dictionario
    # print(**post.dict())
    new_post = models.Post(**post.dict())

    # add the post to the DB
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
   
    return {"data": new_post}



# 8 # GET: Get one post id function
@app.get("/posts/{id}")
# Validacion int: fastapi convierte el id en interos y Respose valida los erroges
def  get_post(id: str, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)
    
    # 9 Error handler de 3 formas distintas
    if not post:

        # 3 tercera forma
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id: {[id]} was not found!"}

    #print(post)
    return {"Post_datail": post}



# 10 DELET: Function to delete one post. busca un id index y lo borra del array
@app.delete("/posts/{id}")
def delete_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    print(post)
    
    #Validacion por si el id que se quiere borrar no existe
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} do not exist")

    #
    post.delete(synchronize_session=False)
    db.commit()

    #Al borrar un post manda un status code pero no devuelve ningun mensaje
    return Response(status_code=status.HTTP_404_NOT_FOUND)

 

# 11 # UPDARE: Update one post id function
@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post,  db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    # print(post)    
    post = post_query.first()

    #Validacion por si el id que se quiere actualizar no existe
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} do not exist")

    # pero si existe le pasamod los campo en forma de dictionario
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return {"data": post_query.first()}

# Documentacion
    # para la documentacion de  tu api con fastApi es simple
    # http://127.0.0.1:8000/docs
    # http://127.0.0.1:8000/redoc
