from sqlalchemy import ForeignKey, MetaData, Table, Column, Integer, String, Date
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

'''
Авторы			
id Автора	ФИО Автора                          Национальность Автора	Дата Рождения Автора
1	        Грибоедов Чебурек Чебурекович	    Таджик	                02.12.1993
2	        Пушкин Владимир Опростоволосович	Сюрстреминг	            15.07.1998
'''
class AuthorsOrm(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    nationality: Mapped[str]
    birthdate: Mapped[date]

'''
Жанры
id Жанра    Жанр	    Описание
1	        Фантастика  О будущем
2           Романтика   О романтичном
'''
class GenresOrm(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(100))

'''
Книги								
id Книги	Название	Язык	    Кол-во страниц  Цена    Оценка Критиков (мин - 0, макс - 10)	Возрастное Ограничение	id Жанра	id Автора
1	        Основы БД	Китайский	10000	        1500	10	                                    18+	                    1	        1
2	        "1984"	    Русский	    252	            2000	8	                                    16+	                    2	        2
'''
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

authors_table = Table(
    "authors",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("full_name", String),
    Column("nationality", String),
    Column("birthdate", Date)
)