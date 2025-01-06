from fastapi import APIRouter, Depends, HTTPException
from queries.core import AsyncCore
from schemas import AuthorsAddDTO, AuthorsUpdateDTO


router = APIRouter(tags=["authors"])

@router.get("/authors")
async def get_authors():
    authors = await AsyncCore.select_authors()
    
    return authors

@router.post("/authors")
async def create_author(author: AuthorsAddDTO = Depends()):
    new_author_id = await AsyncCore.insert_author(author=author)

    return {"id": new_author_id}

@router.put("/authors/{id}")
async def update_auhtor(id: int, update_data: AuthorsUpdateDTO = Depends()):
    updated_author_id = await AsyncCore.update_author(author_id=id, update_data=update_data)

    return {"id": updated_author_id}

@router.delete("/authors/{id}")
async def delete_author(id: int):
    deleted_author_id = await AsyncCore.delete_author(author_id=id)

    if not deleted_author_id:
        raise HTTPException(404, "Пользователь с таким id не найден!") 

    return {"id": id}