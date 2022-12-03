# 1 invocacion de fastapi y methodos adicionales
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schema, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

# Ruta con dependencia para manejar los votos
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schema.Votes, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with the id {vote.post_id} do not exitst")
    

    # Sentencia para encontrar un post
    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == vote.post_id, 
        models.Votes.user_id == current_user.id 
        )

    found_vote = vote_query.first()

    # Si el user provide una direcion 1 has esto:
    if (vote.dir == 1):
        # si el user quiere dar like al post pero este ya ha dido encontrado, este no podra votarlo otra  ves mas
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user{current_user.id} has alredy voted this post {vote.post_idr}")

        #pero si no se ha votado sobre este pos entonces:
        new_vote = models.Votes(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added Vote"}

    else:
        #Pero si el user provide una direcion 0 has esto:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote do no exist")

        # Pero si se encuentra un vote
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted Vote"}
