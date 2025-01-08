from fastapi import APIRouter, Depends, HTTPException
from queries.core import AsyncCore
from schemas import LibrariesAddDTO, LibrariesUpdateDTO, LibrariesDTO
from models import libraries


router = APIRouter(tags=["Libraries"])

@router.get("/Libraries")
async def get_Libraries():
    libraries_list = await AsyncCore.select(libraries, LibrariesDTO)
    
    return libraries_list

@router.post("/Libraries")
async def create_library(library: LibrariesAddDTO = Depends()):
    new_library_id = await AsyncCore.insert(libraries, library)

    return {"id": new_library_id}

@router.put("/Libraries/{id}")
async def update_library(id: int, update_data: LibrariesUpdateDTO = Depends()):
    updated_library_id = await AsyncCore.update(libraries, id, update_data)

    return {"id": updated_library_id}

@router.delete("/Libraries/{id}")
async def delete_library(id: int):
    deleted_library_id = await AsyncCore.delete(libraries, id)

    if not deleted_library_id:
        raise HTTPException(404, "Библиотека с таким id не найдена!") 

    return {"id": id}