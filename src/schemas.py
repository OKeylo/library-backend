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

class DiscountsAddDTO(BaseModel):
    subscription: str
    sub_level: int
    discount_value: int

class DiscountsDTO(DiscountsAddDTO):
    pass

class DiscountsUpdateDTO(BaseModel):
    discount_value: Optional[int] = None

class UsersAddDTO(BaseModel):
    full_name: str
    phone: str
    password: str
    email: Optional[str] = None
    subscription: Optional[str] = None
    sub_level: Optional[int] = None
    birth_date: date

class UsersDTO(UsersAddDTO):
    id: int
    is_admin: bool

class UsersUpdateDTO(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    subscription: Optional[str] = None
    sub_level: Optional[int] = None
    birth_date: Optional[date] = None

class BooksAddDTO(BaseModel):
    name: str
    language: str
    page_number: int
    price: int
    rating: int
    age_limit: int
    id_genre: Optional[int] = None
    id_author: Optional[int] = None

class BooksDTO(BooksAddDTO):
    id: int

class BooksUpdateDTO(BaseModel):
    name: Optional[str] = None
    language: Optional[str] = None
    page_number: Optional[int] = None
    price: Optional[int] = None
    rating: Optional[int] = None
    age_limit: Optional[int] = None
    id_genre: Optional[int] = None
    id_author: Optional[int] = None

class BookAmountsAddDTO(BaseModel):
    library_id: int
    book_id: int
    quantity: int

class BookAmountsDTO(BookAmountsAddDTO):
    pass

class BookAmountsUpdateDTO(BaseModel):
    quantity: Optional[int] = None

class BookTransactionsAddDTO(BaseModel):
    library_id: int
    user_id: int
    book_id: int

class BookTransactionsDTO(BookTransactionsAddDTO):
    id: int

class BookTransactionsUpdateDTO(BaseModel):
    issue_date: Optional[date] = None
    return_date: Optional[date] = None

class BooksAuthorGenreDTO(BaseModel):
    id: int
    name: str
    language: str
    price: int
    rating: int
    age_limit: int
    author_full_name: str
    genre_name: str

