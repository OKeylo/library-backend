from fastapi import APIRouter, Depends, HTTPException
from queries.core import AsyncCore
from schemas import BookTransactionsAddDTO, BookTransactionsUpdateDTO, BookTransactionsDTO
from models import book_transactions

router = APIRouter(tags=["book_transactions"])

@router.get("/book_transactions")
async def get_book_transactions():
    book_transactions_list = await AsyncCore.select(book_transactions, BookTransactionsDTO)
    return book_transactions_list

@router.post("/book_transactions")
async def create_book_transaction(book_transaction: BookTransactionsAddDTO = Depends()):
    new_book_transaction_id = await AsyncCore.insert(book_transactions, book_transaction)
    return {"id": new_book_transaction_id}

@router.put("/book_transactions/{id}")
async def update_book_transaction(id: int, update_data: BookTransactionsUpdateDTO = Depends()):
    updated_book_transaction_id = await AsyncCore.update(book_transactions, id, update_data)
    return {"id": updated_book_transaction_id}

@router.delete("/book_transactions/{id}")
async def delete_book_transaction(id: int):
    deleted_book_transaction_id = await AsyncCore.delete(book_transactions, id)

    if not deleted_book_transaction_id:
        raise HTTPException(404, "Запись о транзакции с таким id не найдена!") 

    return {"id": id}

@router.post("/book_transactions_user")
async def create_book_transaction(book_transaction: BookTransactionsAddDTO = Depends()):
    new_book_transaction_id = await AsyncCore.take_book(book_transaction)
    return {"id": new_book_transaction_id}