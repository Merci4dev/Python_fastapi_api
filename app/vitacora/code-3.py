# 1 invocacion de fastapi y methodos adicionales
from fastapi import FastAPI, Response, status, HTTPException
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
    rating: Optional[int] = None # opcional field


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
def get_posts():

    #14 ejecutando sentencia sql para obterner todos los post de la DB.
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    
    return {'data': posts}


# CREATE: Create post function
# status_code=status.HTTP_201_CREATED (permite cambiar el stado del codigo arrojado)
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    
    #15 inset a post into the DB
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()

    #16 para guardar los post dentro de la DB
    conn.commit()
   
    return {"data": new_post}



# 8 # GET: Get one post id function
@app.get("/posts/{id}")
# Validacion int: fastapi convierte el id en interos y Respose valida los erroges
def  get_post(id: int, response: Response):

    # cursor.execute(""" SELECT * FROM posts WHERE id = 1""")
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))

    post  = cursor.fetchone()
    print(post)

    # 9 usando la funcion para encontrar un post
    print(type(id))
    post = find_post(int(id))
    
    # 9 Error handler de 3 formas distintas
    if not post:

        # 3 tercera forma
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id: {[id]} was not found!"}

    #print(post)
    return {"Post_datail": post}



# 10 DELET: Function to delete one post. busca un id index y lo borra del array
@app.delete("/posts/{id}")
def delete_post(id: int, response: Response):

    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()

    #Validacion por si el id que se quiere borrar no existe
    if delete_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} do not exist")

    #Al borrar un post manda un status code pero no devuelve ningun mensaje
    return Response(status_code=status.HTTP_404_NOT_FOUND)

 

# 11 # UPDARE: Update one post id function
@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s,  published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))

    updated_post = cursor.fetchone()
    conn.commit()

    #Validacion por si el id que se quiere actualizar no existe
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} do not exist")

    return {"data": updated_post}

# Documentacion
    # para la documentacion de  tu api con fastApi es simple
    # http://127.0.0.1:8000/docs
    # http://127.0.0.1:8000/redoc
