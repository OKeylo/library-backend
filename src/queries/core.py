from database import async_engine
from sqlalchemy import Integer, String, bindparam, text, insert, select, update
import asyncio
from models import metadata_obj, authors
from schemas import (
    AuthorsAddDTO, AuthorsDTO, AuthorsUpdateDTO,
    GenresAddDTO, GenresDTO, GenresUpdateDTO,
    LibrariesAddDTO, LibrariesDTO, LibrariesUpdateDTO
)

class AsyncCore:
    @staticmethod
    async def create_tables():
        # sync_engine.echo = False
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)
        # sync_engine.echo = True

    @staticmethod
    async def insert_author(author: AuthorsAddDTO):
        async with async_engine.connect() as conn:
            stmt = """
                INSERT INTO authors (full_name, nationality, birth_date)
                VALUES
                    (:full_name, :nationality, :birth_date)
                RETURNING id;
            """
            
            result = await conn.execute(
                text(stmt),
                {
                    "full_name": author.full_name,
                    "nationality": author.nationality,
                    "birth_date": author.birth_date
                }
            )
            author_id = result.fetchone()[0]
            
            await conn.commit()

            return author_id
        
            # stmt = insert(authors).values(
            #     [
            #         {"full_name": "Грибоедов Чебурек Чебурекович", "nationality": "Таджик", "birthdate": "1993-12-02"},
            #         {"full_name": "Пушкин Владимир Опростоволосович", "nationality": "Сюрстреминг", "birthdate": "1998-07-15"},
            #     ]
            # )
            # conn.execute(stmt)
            # conn.commit()

    @staticmethod
    async def select_authors():
        async with async_engine.connect() as conn:
            # query = select(authors)
            # result = conn.execute(query)
            # workers = result.all()

            stmt = "SELECT * FROM authors"
            res = await conn.execute(text(stmt))
            result_core = res.fetchall()
            result_dto = [AuthorsDTO.model_validate(row, from_attributes=True) for row in result_core]

            print(result_core)
            print(result_dto)

            return result_dto

    @staticmethod
    async def update_author(author_id: int, update_data: AuthorsUpdateDTO):
        async with async_engine.connect() as conn:
            fields_to_update = []
            params = {"id": author_id}

            for field, value in update_data.model_dump(exclude_unset=True).items():
                if value is not None:
                    fields_to_update.append(f"{field} = :{field}")
                    params[field] = value

            if not fields_to_update:
                return author_id
            
            set_clause = ", ".join(fields_to_update)
            stmt = f"UPDATE authors SET {set_clause} WHERE id = :id"

            await conn.execute(text(stmt), params)
            
            await conn.commit()

            return author_id

            # stmt = (
            #     update(authors)
            #     .values(nationality=new_nationality)
            #     #.where(authors_table.c.id==author_id)
            #     .filter_by(id=author_id)
            # )
            # conn.execute(stmt)
            # conn.commit()
    
    @staticmethod
    async def delete_author(author_id: int):
        async with async_engine.connect() as conn:
            stmt = "DELETE FROM authors WHERE id = :id"

            result = await conn.execute(text(stmt), {"id": author_id})

            if result.rowcount == 0:
                return None
            
            await conn.commit()

            return author_id
        
    @staticmethod
    async def insert_genre(genre: GenresAddDTO):
        async with async_engine.connect() as conn:
            stmt = """
                INSERT INTO genres (name, description)
                VALUES
                    (:name, :description)
                RETURNING id;
            """
            
            result = await conn.execute(
                text(stmt),
                {
                    "name": genre.name,
                    "description": genre.description,
                }
            )
            genre_id = result.fetchone()[0]
            
            await conn.commit()

            return genre_id

    @staticmethod
    async def select_genres():
        async with async_engine.connect() as conn:

            stmt = "SELECT * FROM genres"
            res = await conn.execute(text(stmt))
            result_core = res.fetchall()
            result_dto = [GenresDTO.model_validate(row, from_attributes=True) for row in result_core]

            print(result_core)
            print(result_dto)

            return result_dto

    @staticmethod
    async def update_genre(genre_id: int, update_data: GenresUpdateDTO):
        async with async_engine.connect() as conn:
            fields_to_update = []
            params = {"id": genre_id}

            for field, value in update_data.model_dump(exclude_unset=True).items():
                if value is not None:
                    fields_to_update.append(f"{field} = :{field}")
                    params[field] = value

            if not fields_to_update:
                return genre_id
            
            set_clause = ", ".join(fields_to_update)
            stmt = f"UPDATE genres SET {set_clause} WHERE id = :id"

            await conn.execute(text(stmt), params)
            
            await conn.commit()

            return genre_id
    
    @staticmethod
    async def delete_genre(genre_id: int):
        async with async_engine.connect() as conn:
            stmt = "DELETE FROM genres WHERE id = :id"

            result = await conn.execute(text(stmt), {"id": genre_id})

            if result.rowcount == 0:
                return None
            
            await conn.commit()

            return genre_id
        
    @staticmethod
    async def insert_library(library: LibrariesAddDTO):
        async with async_engine.connect() as conn:
            stmt = """
                INSERT INTO libraries (address, phone, email, director_full_name)
                VALUES
                    (:address, :phone, :email, :director_full_name)
                RETURNING id;
            """
            
            result = await conn.execute(
                text(stmt),
                {
                    "address": library.address,
                    "phone": library.phone,
                    "email": library.email,
                    "director_full_name": library.director_full_name
                }
            )
            library_id = result.fetchone()[0]
            
            await conn.commit()

            return library_id

    @staticmethod
    async def select_libraries():
        async with async_engine.connect() as conn:

            stmt = "SELECT * FROM libraries"
            res = await conn.execute(text(stmt))
            result_core = res.fetchall()
            result_dto = [LibrariesDTO.model_validate(row, from_attributes=True) for row in result_core]

            print(result_core)
            print(result_dto)

            return result_dto

    @staticmethod
    async def update_library(library_id: int, update_data: GenresUpdateDTO):
        async with async_engine.connect() as conn:
            fields_to_update = []
            params = {"id": library_id}

            for field, value in update_data.model_dump(exclude_unset=True).items():
                if value is not None:
                    fields_to_update.append(f"{field} = :{field}")
                    params[field] = value

            if not fields_to_update:
                return library_id
            
            set_clause = ", ".join(fields_to_update)
            stmt = f"UPDATE libraries SET {set_clause} WHERE id = :id"

            await conn.execute(text(stmt), params)
            
            await conn.commit()

            return library_id
    
    @staticmethod
    async def delete_library(library_id: int):
        async with async_engine.connect() as conn:
            stmt = "DELETE FROM libraries WHERE id = :id"

            result = await conn.execute(text(stmt), {"id": library_id})

            if result.rowcount == 0:
                return None
            
            await conn.commit()

            return library_id
