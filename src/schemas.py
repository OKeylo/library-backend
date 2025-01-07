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

class GenresAddDTO(BaseModel):
    name: str
    description: str

class GenresDTO(GenresAddDTO):
    id: int

class GenresUpdateDTO(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class LibrariesAddDTO(BaseModel):
    address: str
    phone: str
    email: str
    director_full_name: str

class LibrariesDTO(GenresAddDTO):
    id: int

class LibrariesUpdateDTO(BaseModel):
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    director_full_name: Optional[str] = None



