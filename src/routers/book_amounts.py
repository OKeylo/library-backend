from fastapi import APIRouter, Depends, HTTPException
from queries.core import AsyncCore
from schemas import BookAmountsAddDTO, BookAmountsUpdateDTO, BookAmountsDTO
from models import book_amounts

router = APIRouter(tags=["book_amounts"])

@router.get("/book_amounts")
async def get_book_amounts():
    book_amounts_list = await AsyncCore.select(book_amounts, BookAmountsDTO)
    return book_amounts_list

@router.post("/book_amounts")
async def create_book_amount(book_amount: BookAmountsAddDTO = Depends()):
    new_book_amount = await AsyncCore.insert_book_amounts(book_amount)
    return new_book_amount

@router.put("/book_amounts/{library_id}/{book_id}")
async def update_book_amount(library_id: int, book_id: int, update_data: BookAmountsUpdateDTO = Depends()):
    updated_book_amount_id = await AsyncCore.update(book_amounts, library_id, book_id, update_data)
    return updated_book_amount_id

@router.delete("/book_amounts/{library_id}/{book_id}")
async def delete_book_amount(library_id: int, book_id: int):
    deleted_book_amount_id = await AsyncCore.delete(book_amounts, (library_id, book_id))

    if not deleted_book_amount_id:
        raise HTTPException(404, "Запись о количестве книги не найдена!") 

    return {"library_id": library_id, "book_id": book_id}
