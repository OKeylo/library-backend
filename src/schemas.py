from pydantic import BaseModel
from datetime import date

class AuthorsAddDTO(BaseModel):
    full_name: str
    nationality: str
    birth_date: date

class AuthorsDTO(AuthorsAddDTO):
    id: int