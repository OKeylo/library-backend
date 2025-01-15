from sqlalchemy import ForeignKey, ForeignKeyConstraint, MetaData, PrimaryKeyConstraint, Table, Column, Integer, String, BigInteger, Date, SmallInteger, CheckConstraint, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, timedelta

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
    Column("discount_value", Integer, CheckConstraint("discount_value >= 0 AND discount_value <= 100"), nullable=False),
    PrimaryKeyConstraint("subscription", "sub_level")
)

users = Table(
    "users", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("full_name", String(100), nullable=False),
    Column("phone", String(12), unique=True, nullable=False),
    Column("password", String(100), nullable=False),
    Column("is_admin", Boolean, nullable=False, server_default="0"),
    Column("subscription", String(50), nullable=True, server_default="Basic"),
    Column("sub_level", Integer, nullable=True, server_default="1"),
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
    Column("age_limit", Integer, CheckConstraint("age_limit >= 0 AND age_limit <= 19"), nullable=False),
    Column("id_genre", Integer, ForeignKey("genres.id"), nullable=True),
    Column("id_author", Integer, ForeignKey("authors.id"), nullable=True)
)

book_amounts = Table(
    "book_amounts", metadata_obj,
    Column("library_id", Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False),
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False),
    Column("quantity", Integer, CheckConstraint("quantity >= 0"), nullable=False),
    PrimaryKeyConstraint("library_id", "book_id")
)

def default_return_date():
    return func.current_date() + timedelta(days=30)

book_transactions = Table(
    "book_transactions", metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("library_id", Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False),
    Column("issue_date", Date, nullable=False, server_default=func.current_date()),
    Column("return_date", Date, nullable=False, server_default=func.current_date() + 40)
)
