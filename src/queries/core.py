from database import sync_engine, async_engine
from sqlalchemy import Integer, String, bindparam, text, insert, select, update
import asyncio
from models import authors_table

class SyncCore:
    @staticmethod
    def get_123_sync():
        with sync_engine.connect() as conn:
            res = conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
            print(f"{res.all()=}")
    
    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
            # stmt = """
            #     INSERT INTO authors (full_name,nationality,birthdate)
            #     VALUES
            #         ('Грибоедов Чебурек Чебурекович', 'Таджик', '1993-12-02'),
            #         ('Пушкин Владимир Опростоволосович', 'Сюрстреминг', '1998-07-15');
            # """
            # conn.execute(text(stmt))
            
            stmt = insert(authors_table).values(
                [
                    {"full_name": "Грибоедов Чебурек Чебурекович", "nationality": "Таджик", "birthdate": "1993-12-02"},
                    {"full_name": "Пушкин Владимир Опростоволосович", "nationality": "Сюрстреминг", "birthdate": "1998-07-15"},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_authors():
        with sync_engine.connect() as conn:
            query = select(authors_table)
            result = conn.execute(query)
            workers = result.all()

            print(f"{workers}")

    @staticmethod
    def update_author(author_id: int = 2, new_nationality: str = "Русский"):
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE authors SET nationality=:nationality WHERE id=:id")
            # conn.execute(stmt, {"nationality": new_nationality, "id": author_id})
            stmt = (
                update(authors_table)
                .values(nationality=new_nationality)
                #.where(authors_table.c.id==author_id)
                .filter_by(id=author_id)
            )
            conn.execute(stmt)
            conn.commit()


async def get_123():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT 1,2,3 union select 4,5,6"))
        print(f"{res.all()=}")

asyncio.run(get_123())

# def create_tables():
#     sync_engine.echo = False
#     metadata_obj.drop_all(sync_engine)
#     metadata_obj.create_all(sync_engine)
#     sync_engine.echo = True

