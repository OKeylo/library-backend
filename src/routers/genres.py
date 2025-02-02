from fastapi import APIRouter, Depends, HTTPException
from queries.core import AsyncCore
from schemas import GenresAddDTO, GenresUpdateDTO, GenresDTO
from models import genres
from models_auth.auth_bearer import JWTBearer


router = APIRouter(tags=["genres"])

@router.get("/genres")
async def get_genres():
    genres_list = await AsyncCore.select(genres, GenresDTO)
    
    return genres_list

@router.post("/genres", dependencies=[Depends(JWTBearer())])
async def create_genre(author: GenresAddDTO):
    new_author_id = await AsyncCore.insert(genres, author)

    return {"id": new_author_id}

@router.put("/genres/{id}", dependencies=[Depends(JWTBearer())])
async def update_genre(id: int, update_data: GenresUpdateDTO):
    updated_author_id = await AsyncCore.update(genres, id, update_data)

    return {"id": updated_author_id}

@router.delete("/genres/{id}", dependencies=[Depends(JWTBearer())])
async def delete_genre(id: int):
    deleted_author_id = await AsyncCore.delete(genres, id)

    if not deleted_author_id:
        raise HTTPException(404, "Жанр с таким id не найден!") 

    return {"id": id}