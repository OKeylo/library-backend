from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from queries.core import AsyncCore
from database import async_engine
from routers import authors, libraries, discounts, genres, users, books, book_amounts, book_transactions
import re
from sqlalchemy.exc import SQLAlchemyError

@asynccontextmanager
async def lifespan(app: FastAPI):
    await AsyncCore.create_tables()
    await AsyncCore.insert_all()
    print("База данных готова")

    yield

    await async_engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
)

app.include_router(authors.router)
app.include_router(libraries.router)
app.include_router(discounts.router)
app.include_router(genres.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(book_amounts.router)
app.include_router(book_transactions.router)

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc: SQLAlchemyError):
    error_message = str(exc.__dict__["orig"])

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": error_message}
    )