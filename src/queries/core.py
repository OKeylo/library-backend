from typing import Type
from fastapi import HTTPException, status
from pydantic import BaseModel
from database import async_engine
from sqlalchemy import Integer, String, Table, and_, bindparam, delete, text, insert, select, update, asc, desc
import asyncio
from models import metadata_obj, authors, discounts, books, genres, users, book_transactions, book_amounts
from schemas import (
    DiscountsAddDTO, DiscountsDTO, DiscountsUpdateDTO, BooksAuthorGenreDTO, UsersAddDTO, BookTransactionsAddDTO, BookAmountsUpdateDTO
)
from sqlalchemy.exc import SQLAlchemyError

class AsyncCore:
    @staticmethod
    async def create_tables():
        # sync_engine.echo = False
        async with async_engine.begin() as conn:
            await conn.run_sync(metadata_obj.drop_all)
            await conn.run_sync(metadata_obj.create_all)
        # sync_engine.echo = True

    @staticmethod
    async def insert_all():
        async with async_engine.connect() as conn:  # Начало транзакции
            # Вставка в таблицу libraries (теперь только 2 библиотеки)
            # Вставка в таблицу libraries (теперь только 2 библиотеки)
            await conn.execute(text("""
                INSERT INTO libraries (address, phone, email, director_full_name)
                VALUES
                ('Moscow, Tverskaya, 1', '1234567890', 'library@example.com', 'Ivan Ivanov'),
                ('Saint Petersburg, Nevsky Prospect, 50', '0987654321', 'contact@library.com', 'Olga Petrovna');
            """))

            # Вставка в таблицу genres
            await conn.execute(text("""
                INSERT INTO genres (name, description)
                VALUES
                ('Fiction', 'A literary genre that includes imaginative or invented content'),
                ('Science', 'Books that focus on scientific topics and theories'),
                ('Fantasy', 'Fictional books involving magical or supernatural elements'),
                ('Non-fiction', 'Books that are based on facts and real events'),
                ('Mystery', 'Fictional works involving a crime or puzzle to be solved');
            """))

            # Вставка в таблицу authors
            await conn.execute(text("""
                INSERT INTO authors (full_name, nationality, birth_date)
                VALUES
                ('Leo Tolstoy', 'Russian', '1828-09-09'),
                ('Isaac Newton', 'English', '1643-01-04'),
                ('J.K. Rowling', 'British', '1965-07-31'),
                ('Stephen King', 'American', '1947-09-21'),
                ('Agatha Christie', 'British', '1890-09-15');
            """))

            # Вставка в таблицу discounts
            await conn.execute(text("""
                INSERT INTO discounts (subscription, sub_level, discount_value)
                VALUES
                ('Basic', 1, 5),
                ('Premium', 2, 15),
                ('Gold', 3, 20),
                ('Platinum', 4, 25),
                ('Student', 5, 30);
            """))

            # Вставка в таблицу users
            await conn.execute(text("""
                INSERT INTO users (full_name, phone, password, email, subscription, sub_level, birth_date)
                VALUES
                ('Alexey Ivanov', 12345678901, '123', 'alexey@mail.com', 'Basic', 1, '1995-05-15'),
                ('Maria Petrova', 98765432100, '136', 'maria@mail.com', 'Premium', 2, '1992-08-22'),
                ('Dmitry Fedorov', 555888777, '22952', 'dmitry@mail.com', 'Gold', 3, '1988-03-10'),
                ('Olga Smirnova', 666777888, '8122', 'olga@mail.com', 'Student', 5, '2000-12-01'),
                ('Ivan Kuznetsov', 777666555, '211', 'ivan@mail.com', 'Platinum', 4, '1990-06-14');
            """))

            # Вставка в таблицу books
            await conn.execute(text("""
                INSERT INTO books (name, language, page_number, price, rating, age_limit, id_genre, id_author)
                VALUES
                ('War and Peace', 'Russian', 1225, 500, 10, 19, 1, 1),
                ('Principia Mathematica', 'English', 600, 1000, 9, 13, 2, 2),
                ('Harry Potter and the Philosopher''s Stone', 'English', 320, 400, 9, 7, 3, 3),
                ('The Shining', 'English', 650, 700, 8, 19, 5, 4),
                ('Murder on the Orient Express', 'English', 320, 350, 9, 17, 5, 5),
                ('The Catcher in the Rye', 'English', 277, 300, 8, 17, 4, 1),
                ('1984', 'English', 328, 400, 9, 17, 4, 2),
                ('The Hobbit', 'English', 310, 500, 10, 13, 3, 3),
                ('It', 'English', 1138, 800, 9, 19, 5, 4),
                ('Sherlock Holmes: The Complete Collection', 'English', 2800, 1500, 10, 17, 5, 5);
            """))

            # Вставка в таблицу book_amounts
            await conn.execute(text("""
                INSERT INTO book_amounts (library_id, book_id, quantity)
                VALUES
                (1, 1, 10),
                (1, 2, 5),
                (2, 3, 15),
                (2, 4, 7),
                (1, 5, 8),
                (1, 6, 0),
                (2, 7, 12),
                (2, 8, 10),
                (1, 9, 6),
                (1, 10, 20);
            """))

            # Вставка в таблицу book_transactions
            await conn.execute(text("""
                INSERT INTO book_transactions (library_id, user_id, book_id)
                VALUES
                (1, 1, 1),
                (2, 2, 3),
                (1, 3, 5),
                (2, 4, 7),
                (1, 5, 9),
                (1, 2, 4),
                (2, 3, 6),
                (1, 1, 2),
                (2, 5, 8),
                (1, 4, 10);
            """))

            await conn.commit()

    @staticmethod
    async def insert(table: Table, dto: BaseModel):
        data = dto.model_dump(exclude_unset=True)

        async with async_engine.connect() as conn:
            stmt = insert(table).values(data).returning(table.c.id)
            result = await conn.execute(stmt)
            record_id = result.fetchone()[0]
            
            await conn.commit()
            
        return record_id
    
    @staticmethod
    async def select(table: Table, dto: Type[BaseModel]):
        async with async_engine.connect() as conn:
            stmt = select(table)
            res = await conn.execute(stmt)
            result_core = res.fetchall()

            result_dto = [dto.model_validate(row, from_attributes=True) for row in result_core]
            
            return result_dto

    @staticmethod
    async def update(table: Table, record_id: int, dto: BaseModel):
        data = dto.model_dump(exclude_unset=True)

        data = {key: value for key, value in data.items() if value is not None}

        if not data:
            return record_id

        async with async_engine.connect() as conn:
            stmt = (
                update(table)
                .where(table.c.id == record_id)
                .values(data)
                .returning(table.c.id)
            )
            await conn.execute(stmt)
            await conn.commit()

        return record_id
    
    @staticmethod
    async def delete(table: Table, record_id: int):
        async with async_engine.connect() as conn:
            stmt = delete(table).where(table.c.id == record_id)
            result = await conn.execute(stmt)
            if result.rowcount == 0:
                return None
            await conn.commit()

        return record_id
    
    @staticmethod
    async def insert_discount(dto: DiscountsAddDTO):
        data = dto.model_dump(exclude_unset=True)

        async with async_engine.connect() as conn:
            stmt = insert(discounts).values(data).returning(discounts.c.subscription, discounts.c.sub_level)
            result = await conn.execute(stmt)
            subscription, sub_level = result.fetchone()
            
            await conn.commit()

        return {"subscription": subscription, "sub_level": sub_level}
    
    @staticmethod
    async def update_discount(subscription: str, sub_level: int, dto: DiscountsUpdateDTO):
        data = dto.model_dump(exclude_unset=True)

        data = {key: value for key, value in data.items() if value is not None}

        if not data:
            return {"subscription": subscription, "sub_level": sub_level}

        async with async_engine.connect() as conn:
            stmt = (
                update(discounts)
                .where(and_(
                    discounts.c.subscription == subscription,
                    discounts.c.sub_level == sub_level
                ))
                .values(data)
                .returning(discounts.c.subscription, discounts.c.sub_level)
            )
            await conn.execute(stmt)
            await conn.commit()

        return {"subscription": subscription, "sub_level": sub_level}
    
    @staticmethod
    async def delete_discount(subscription: str, sub_level: int):
        async with async_engine.connect() as conn:
            stmt = delete(discounts).where(and_(discounts.c.subscription == subscription, discounts.c.sub_level == sub_level))
            result = await conn.execute(stmt)
            if result.rowcount == 0:
                return None
            await conn.commit()

        return {"subscription": subscription, "sub_level": sub_level}
    
    @staticmethod
    async def select_books_with_parameters(sort_field: str = "id", sort_order: str = "desc", name_contains: str = None, filter_field: str = "", filter_value: str = None):
        available_columns = [col for col in books.columns.keys() if col not in ['id_author', 'id_genre']]
        available_columns += ['author_full_name', 'genre_name']
        
        if sort_field not in available_columns:
            raise HTTPException(400 ,f"Неверное имя поля. Возможные поля: {', '.join(available_columns)}")
        
        if sort_order not in ["asc", "desc"]:
            raise HTTPException(400, "НЕверный порядок сортирвки. Используйте 'asc' или 'desc'.")

        if filter_field and filter_field not in available_columns:
            raise HTTPException(400, f"Неверное имя поля для фильтрации: {filter_field}. Возможные поля: {', '.join(available_columns)}")

        order_clause = asc if sort_order == "asc" else desc
        sort_column = getattr(books.c, sort_field)

        filter_column = getattr(books.c, filter_field, None)

        if filter_column is not None:
            column_type = filter_column.type

        async with async_engine.begin() as conn:
            stmt = select(
                books.c.id,
                books.c.name,
                books.c.language,
                books.c.price,
                books.c.rating,
                books.c.age_limit,
                authors.c.full_name.label("author_full_name"),
                genres.c.name.label("genre_name")
            ).join(
                authors, books.c.id_author == authors.c.id, isouter=True
            ).join(
                genres, books.c.id_genre == genres.c.id, isouter=True
            )

            if name_contains:
                stmt = stmt.where(books.c.name.ilike(f"%{name_contains}%"))

            if filter_field and filter_value:
                if isinstance(column_type, String):
                    stmt = stmt.where(filter_column.ilike(f"%{filter_value}%"))
                elif isinstance(column_type, Integer):
                    stmt = stmt.where(filter_column == int(filter_value))
                else:
                    raise HTTPException(400, f"Неподдерживаемый тип для фильтрации: {column_type}")

            stmt = stmt.order_by(order_clause(sort_column))

            res = await conn.execute(stmt)
            result_core = res.fetchall()

            result_dto = [BooksAuthorGenreDTO.model_validate(row, from_attributes=True) for row in result_core]
        
        return result_dto
    
    @staticmethod
    async def create_user_by_phone(new_user: UsersAddDTO):
        new_user_data = new_user.model_dump(exclude_unset=True)

        async with async_engine.begin() as conn:
            stmt = select(users).where(users.c.phone == new_user_data["phone"])
            res = await conn.execute(stmt)
            result_core = res.fetchone()

            if result_core:
                raise HTTPException(409, f"Пользователь с номером телефона {new_user_data["phone"]} уже существует.")

            stmt_insert = insert(users).values(new_user_data).returning(users.c.id)
            res_insert = await conn.execute(stmt_insert)
            new_user_id = res_insert.fetchone()[0]

        return new_user_id
    
    @staticmethod
    async def take_book(transaction: BookTransactionsAddDTO):
        transaction = transaction.model_dump(exclude_unset=True)

        async with async_engine.begin() as conn:
            stmt_update = (
                update(book_amounts)
                .where(and_(
                    book_amounts.c.library_id == transaction["library_id"],
                    book_amounts.c.book_id == transaction["book_id"]
                ))
                .values(quantity = book_amounts.c.quantity - 1))
            await conn.execute(stmt_update)
            
            stmt_insert = insert(book_transactions).values(transaction).returning(book_transactions.c.id)
            result = await conn.execute(stmt_insert)
            record_id = result.fetchone()[0]
                
        return record_id
    
    @staticmethod
    async def return_book(transaction_id: int):
        transaction = transaction.model_dump(exclude_unset=True)

        async with async_engine.begin() as conn:
            stmt_update = (
                update(book_amounts)
                .where(and_(
                    book_amounts.c.library_id == transaction["library_id"],
                    book_amounts.c.book_id == transaction["book_id"]
                ))
                .values(quantity = book_amounts.c.quantity + 1))
            await conn.execute(stmt_update)
            
            stmt_delete = delete(book_transactions).where(book_transactions.c.id == transaction_id).returning(book_transactions.c.id)
            result = await conn.execute(stmt_delete)
            record_id = result.fetchone()[0]
                
        return record_id