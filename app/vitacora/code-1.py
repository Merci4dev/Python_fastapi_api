# 1 inicializar la app con esta libreria
from fastapi import FastAPI, Response, status, HTTPException
# Extra el cuerpo del post request
from fastapi.params import Body
#5 Para definir el modelo de los datos
from pydantic import BaseModel
from typing import Optional
# para establecer un id rando
from random import randrange

app = FastAPI()

#5 con la librefia pydantic estableceremos el esquema de los datos lo cual estaremos recibiendo de los users. Esto hace la validacion por nosotros
# title str, content str, category, datetime Boll, etc
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None # opcional field


#6 variable global par guardar los posts de forma estatica
my_posts = [
    { 
    "title": "Post title No1",
    "content": "Post content No1",
    "id": 1,
  },
    { 
    "title": "Programar",
    "content": "Quiero aprender a programar rapido",
    "id": 2,
  },
    { 
    "title": "Cocinar",
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



# crea el server /(uvicorn main:app)
# Decorato(especificamos la url)
# @app.get("/loging")

# 2 GET: Function which render the home  
@app.get("/")  
def root():
    return {"message": "Hello World OK"}


# # GET: Get all post function
@app.get("/posts")
def get_posts():
    #return {"date": "this is a post"}
    return {"date": my_posts}

# 4 post request fuction
# Esta func extrae los datos del body y lo convierte en un dictionario y loa guarda en la variable payload
'''
#@app.post("/createpost")
# def create_posts(payload: dict = Body(...)):
    #return {"date": "post succesfully create"}
    #print(payload)
    # f =(convierte los datos a strings)
    #return {"new post": f"title {payload['title']} content: {payload['content']}"}

'''

# CREATE: Create post function
# status_code=status.HTTP_201_CREATED (permite cambiar el stado del codigo arrojado)
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #print(new_post.rating)
    #convirte una variable a un dictionario
    print(post.dict(),"\n")

    # 7 Crea un nuevo post y le Asignando el rendo id a los posts
    post_dict = post.dict()
    post_dict['id'] = randrange(10000, 10000000)
    my_posts.append(post_dict)
    
    return {"data": post_dict}


# 8 # GET: Get one post id function
@app.get("/posts/{id}")
# Validacion int: fastapi convierte el in en interos y Respose valida los erroges
def  get_post(id: int, response: Response):
    #print(id)
    #return {"data": f"Post id: {id}"}
    # 9 usando la funcion para encontrar un post
    print(type(id))
    post = find_post(int(id))
    
    # 9 Error handler
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": "Post id not found!"}

        #Mejora en el errorHandler
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND)
    #print(post)
    return {"Post_datail": post}



# 10 DELET: Function to delete one post. busca un id index y lo borra del array
@app.delete("/posts/{id}", status_code=status.HTTP_404_NOT_FOUND)
def delete_post(id: int):
    index = find_index_post(id)

    #Validacion por si el id que se quiere borrar no existe
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} do not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_404_NOT_FOUND)



# 11 # UPDARE: Update one post id function
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    #Validacion por si el id que se quiere actualizar no existe
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} do not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}

# Documentacion
    # para la documentacion de  tu api con fastApi es simple
    # http://127.0.0.1:8000/docs
    # http://127.0.0.1:8000/redoc
