from sqlalchemy import MetaData, Table, Column, Integer, String, Date
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date


class AuthorsOrm(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str]
    nationality: Mapped[str]
    birthdate: Mapped[date]

# metadata_obj = MetaData()

# authors_table = Table(
#     "authors",
#     metadata_obj,
#     Column("id", Integer, primary_key=True),
#     Column("full_name", String),
#     Column("nationality", String),
#     Column("birthdate", Date)
# )