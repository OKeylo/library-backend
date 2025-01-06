from pydantic import BaseModel
from datetime import date
from typing import Optional

class AuthorsAddDTO(BaseModel):
    full_name: str
    nationality: str
    birth_date: date

class AuthorsDTO(AuthorsAddDTO):
    id: int

class AuthorsUpdateDTO(BaseModel):
    full_name: Optional[str] = None
    nationality: Optional[str] = None
    birth_date: Optional[date] = None