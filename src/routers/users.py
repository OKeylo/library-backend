from fastapi import APIRouter, Depends, HTTPException
from queries.core import AsyncCore
from schemas import UsersAddDTO, UsersUpdateDTO, UsersDTO
from models import users

router = APIRouter(tags=["users"])

@router.get("/users")
async def get_users():
    users_list = await AsyncCore.select(users, UsersDTO)
    return users_list

@router.post("/users")
async def create_user(user: UsersAddDTO = Depends()):
    new_user_id = await AsyncCore.insert(users, user)
    return {"id": new_user_id}

@router.put("/users/{id}")
async def update_user(id: int, update_data: UsersUpdateDTO = Depends()):
    updated_user_id = await AsyncCore.update(users, id, update_data)
    return {"id": updated_user_id}

@router.delete("/users/{id}")
async def delete_user(id: int):
    deleted_user_id = await AsyncCore.delete(users, id)

    if not deleted_user_id:
        raise HTTPException(404, "Пользователь с таким id не найден!") 

    return {"id": id}
