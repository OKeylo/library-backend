import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Request
from models_auth import auth_handler
from models_auth.auth_bearer import JWTBearer
from queries.core import AsyncCore
from schemas import UsersAddDTO, UsersUpdateDTO, UsersDTO, UsersLoginDTO
from models import users
from fastapi.params import Body
from models_auth.auth_handler import signJWT

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

@router.post("/users_phone")
async def create_user(user: UsersAddDTO = Depends()):
    new_user_id = await AsyncCore.create_user_by_phone(user)

    return {"id": new_user_id}

@router.post("/user/signup")
async def create_user(
    user: UsersAddDTO = Body(...)
):
    check_existing_phone = await AsyncCore.get_user_by_phone(user.phone)
    if check_existing_phone:
        raise HTTPException(406, "User with this phone already exists")
    
    user = UsersAddDTO(
        full_name=user.full_name,
        phone=user.phone,
        password=user.password,
        birth_date=user.birth_date
    )

    response = await AsyncCore.add_user(user)
    if response:
        return signJWT(user.phone)
    raise HTTPException(400, "Something went wrong / Bad Request")
    

@router.post("/user/login")
async def user_login(user: UsersLoginDTO = Body(...)):
    response: UsersDTO = await AsyncCore.get_user_by_phone(user.phone)

    if not response:
        return { "error": "Wrong phone!" }
    
    if not bcrypt.checkpw(user.password.encode("utf-8"), response.password.encode("utf-8")):
        return { "error": "Wrong password!" }
    
    return signJWT(user.phone)
    

@router.get("/user/me", dependencies=[Depends(JWTBearer())])
async def get_current_user(request: Request):
    token = request.headers.get("authorization").split(" ")[1]
    user: UsersDTO = await auth_handler.get_user(token)

    if not user:
        raise HTTPException(400, "Something went wrong / Bad Request")

    return user

@router.get("/users/{user_id}")
async def get_user_info(user_id: int):
    try:
        user_info = await AsyncCore.get_user_info(user_id)
        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
