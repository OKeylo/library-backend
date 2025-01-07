from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from queries.core import AsyncCore
from database import async_engine
from routers import authors, libraries

@asynccontextmanager
async def lifespan(app: FastAPI):
    await AsyncCore.create_tables()
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
