import time
from typing import Dict

import jwt

from queries.core import AsyncCore
from schemas import UsersDTO


JWT_SECRET = "your_secret_key"
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user_phone: str) -> Dict[str, str]:
    payload = {
        "user_phone": user_phone,
        "expires": time.time() + 900
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
async def get_user(token: str) -> UsersDTO:
    print(token)
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        #return {"token": decoded_token}
    except jwt.PyJWTError:
        raise

    phone = decoded_token.get("user_phone")

    user = await AsyncCore.get_user_by_phone(phone=phone)
    if not user:
        raise

    return user
