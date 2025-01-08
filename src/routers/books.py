from fastapi import APIRouter, Depends, HTTPException
from queries.core import AsyncCore
from schemas import BooksAddDTO, BooksUpdateDTO, BooksDTO
from models import books
from typing import Optional

router = APIRouter(tags=["books"])

@router.get("/books")
async def get_books():
    books_list = await AsyncCore.select(books, BooksDTO)
    return books_list

@router.post("/books")
async def create_book(book: BooksAddDTO = Depends()):
    new_book_id = await AsyncCore.insert(books, book)
    return {"id": new_book_id}

@router.put("/books/{id}")
async def update_book(id: int, update_data: BooksUpdateDTO = Depends()):
    updated_book_id = await AsyncCore.update(books, id, update_data)
    return {"id": updated_book_id}

@router.delete("/books/{id}")
async def delete_book(id: int):
    deleted_book_id = await AsyncCore.delete(books, id)

    if not deleted_book_id:
        raise HTTPException(404, "Книга с таким id не найдена!") 

    return {"id": id}

@router.get("/books_with_parameters")
async def get_books_with_parameters(
    sort_field: str = "id",
    sort_order: str = "desc",
    name_contains: Optional[str] = None,
    filter_field: str = None,
    filter_value: str = None
):
    books_list = await AsyncCore.select_books_with_parameters(sort_field, sort_order, name_contains, filter_field, filter_value)
    return books_list
