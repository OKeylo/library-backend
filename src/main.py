from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from queries.core import SyncCore
from schemas import AuthorsAddDTO

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
)

@app.get("/authors")
def get_authors():
    authors = SyncCore.select_authors()

    return authors

@app.post("/author")
def create_author(author: AuthorsAddDTO = Depends()):
    new_author_id = SyncCore.insert_author(author=author)

    return {"id": new_author_id}