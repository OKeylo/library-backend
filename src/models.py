from sqlalchemy import ForeignKey, ForeignKeyConstraint, MetaData, PrimaryKeyConstraint, Table, Column, Integer, String, BigInteger, Date, SmallInteger, CheckConstraint
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

"""
Авторы			
id Автора	ФИО Автора                          Национальность Автора	Дата Рождения Автора
1	        Грибоедов Чебурек Чебурекович	    Таджик	                02.12.1993
2	        Пушкин Владимир Опростоволосович	Сюрстреминг	            15.07.1998
"""
class AuthorsOrm(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    nationality: Mapped[str]
    birthdate: Mapped[date]

"""
Жанры
id Жанра    Жанр	    Описание
1	        Фантастика  О будущем
2           Романтика   О романтичном
"""
class GenresOrm(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100))

"""
Книги								
id Книги	Название	Язык	    Кол-во страниц  Цена    Оценка Критиков (мин - 0, макс - 10)	Возрастное Ограничение	id Жанра	id Автора
1	        Основы БД	Китайский	10000	        1500	10	                                    18+	                    1	        1
2	        "1984"	    Русский	    252	            2000	8	                                    16+	                    2	        2
"""
class BooksOrm(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    language: Mapped[str] = mapped_column(String(50))
    number_of_pages: Mapped[int]
    price: Mapped[int]
    critics_assessment: Mapped[int]
    age_limit: Mapped[int]
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))

metadata_obj = MetaData()

libraries = Table(
    "libraries", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("address", String(50), nullable=False),
    Column("phone", String(12), nullable=False),
    Column("email", String(50), nullable=True),
    Column("director_full_name", String(100), nullable=True)
)

genres = Table(
    "genres", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("description", String(100), nullable=False)
)

authors = Table(
    "authors", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("full_name", String(100), nullable=False),
    Column("nationality", String(50), nullable=False),
    Column("birth_date", Date, nullable=False)
)

discounts = Table(
    "discounts", metadata_obj,
    Column("subscription", String(30), nullable=False),
    Column("sub_level", Integer, nullable=False),
    Column("discount_value", Integer, nullable=False),
    PrimaryKeyConstraint("subscription", "sub_level")
)

readers = Table(
    "readers", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("full_name", String(100), nullable=False),
    Column("phone", BigInteger, nullable=False),
    Column("email", String(50), nullable=True),
    Column("subscription", String(50), nullable=True),
    Column("sub_level", Integer, nullable=True),
    Column("birth_date", Date, nullable=False),
    ForeignKeyConstraint(["subscription", "sub_level"], ["discounts.subscription", "discounts.sub_level"], ondelete="SET NULL")
)

books = Table(
    "books", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("language", String(25), nullable=False),
    Column("page_number", SmallInteger, nullable=False),
    Column("price", Integer, nullable=False),
    Column("rating", Integer, CheckConstraint("rating >= 0 AND rating <= 10"), nullable=False),
    Column("age_limit", String(3), nullable=False),
    Column("id_genre", Integer, ForeignKey("genres.id"), nullable=True),
    Column("id_author", Integer, ForeignKey("authors.id"), nullable=True)
)

books_amount = Table(
    "book_amounts", metadata_obj,
    Column("library_id", Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False),
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False),
    Column("quantity", Integer, CheckConstraint("quantity >= 0"), nullable=False),
    PrimaryKeyConstraint("library_id", "book_id")
)

books_transaction = Table(
    "book_transactions", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("library_id", Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False),
    Column("reader_id", Integer, ForeignKey("readers.id", ondelete="CASCADE"), nullable=False),
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False),
    Column("issue_date", Date, nullable=False),
    Column("return_date", Date, nullable=False)
)
