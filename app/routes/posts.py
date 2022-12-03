# POST COMPONENT
# 1 invocacion de fastapi y methodos adicionales
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from sqlalchemy import func
# Importing the model and DB Engine, utils file
from .. import models, schema, oauth2
from .. database import get_db


# Rotes
router = APIRouter(
    # estableciendo el prefijo a la rutas
    prefix="/posts",

    # Añade una etiqueta al grupo del post para la documentacion (http://127.0.0.1:8000/docs)
    tags=["Posts"]
)


# GET: Get all post function
# @router.get('/', response_model=List[schema.Post])
# For the JOIN
@router.get('/', response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    #  make connection with the the DB thow the model ang get all post
    # esta line muestra  todo los post para toso los users
    # posts = db.query(models.Post).all()

    #con esta linea solo se musetran los post corepondiente al user logeado y limitamos el numero de post que quermos mostrar por pabinacion. tambien lo implementamos el skip (para la paginacion). implemtamos el search params
    # %20 (espacio en la url). Se usa para buscar query con espacios 
    posts = db.query(models.Post).filter(
        models.Post.owner_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()


    results = db.query(
        models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id ==  models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.owner_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # print(results)

    return  results
    # return  posts


# CREATE: Create post function
# Aqui definimos el modelo de repuesta
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    # print(current_user.email )

    new_post = models.Post(owner_id=current_user.id, **post.dict())

    # add the post to the DB
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
   
    return new_post



# 8 # GET: Get one post id function
# @router.get("/{id}", response_model=schema.Post)
@router.get("/{id}", response_model=schema.PostOut)
# Validacion int: fastapi convierte el id en interos y Respose valida los erroges
def  get_post(id: int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):

    # post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)

    # Con este cambio podemos mostrar los votes al obtener un solo post
    post = db.query(
        models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes, models.Votes.post_id ==  models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    # 9 Error handler
    if not post:

        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} was not found!")

    # Logica par que el user no puda obtener un post que no le coresponde. si se quieren obtener solo se quita esta linea
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform thid request action")

    #print(post)
    return post



# 10 DELET: Function to delete one post. busca un id index y lo borra del array
@router.delete("/{id}")
def delete_post(id: int, response: Response, db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    #print(post)
    
    post = post_query.first()

    #Validacion por si el id que se quiere borrar no existe
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {[id]} do not exist")

    # Logica par que el user no puda borrar un post que no le coresponde
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform thid request action")

    #
    post_query.delete(synchronize_session=False)
    db.commit()

    #Al borrar un post manda un status code pero no devuelve ningun mensaje
    return Response(status_code=status.HTTP_404_NOT_FOUND)

 

# 11 # UPDARE: Update one post id function
@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, updated_post: schema.PostCreate,  db: Session = Depends(get_db), current_user  : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    # print(post)    
    post = post_query.first()

    #Validacion por si el id que se quiere actualizar no existe
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"Post with id: {id} do not exist")

    # Logica par que el user no puda actulaizar un post que no le coresponde
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform thid request action")

    # pero si existe le pasamos los campo en forma de dictionario
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

# Documentacion
    # para la documentacion de  tu api con fastApi es simple
    # http://127.0.0.1:8000/docs
    # http://127.0.0.1:8000/redoc


