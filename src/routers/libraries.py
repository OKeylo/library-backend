from fastapi import APIRouter, Depends, HTTPException
from queries.core import AsyncCore
from schemas import LibrariesAddDTO, LibrariesUpdateDTO


router = APIRouter(tags=["Libraries"])

@router.get("/Libraries")
async def get_Libraries():
    Libraries = await AsyncCore.select_libraries()
    
    return Libraries

@router.post("/Libraries")
async def create_library(library: LibrariesAddDTO = Depends()):
    new_library_id = await AsyncCore.insert_library(library=library)

    return {"id": new_library_id}

@router.put("/Libraries/{id}")
async def update_library(id: int, update_data: LibrariesUpdateDTO = Depends()):
    updated_library_id = await AsyncCore.update_library(library_id=id, update_data=update_data)

    return {"id": updated_library_id}

@router.delete("/Libraries/{id}")
async def delete_library(id: int):
    deleted_library_id = await AsyncCore.delete_library(library_id=id)

    if not deleted_library_id:
        raise HTTPException(404, "Библиотека с таким id не найдена!") 

    return {"id": id}