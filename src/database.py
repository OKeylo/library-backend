from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings
import asyncio

# sync_engine = create_engine(
#     url=settings.DATABASE_URL_psycopg,
#     echo=True,
#     #pool_size=5,
#     #max_overflow=10
# )

# @event.listens_for(sync_engine, "connect", insert=True)
# def set_current_schema(dbapi_connection, connection_record):
#     cursor_obj = dbapi_connection.cursor()
#     cursor_obj.execute("SET search_path TO %s" % settings.DB_SCHEMA)
#     cursor_obj.close()


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
    pool_size=50,
    max_overflow=10
)

# @event.listens_for(async_engine.sync_engine, "connect", insert=True)
# def set_current_schema(dbapi_connection, connection_record):
#     cursor_obj = dbapi_connection.cursor()
#     cursor_obj.execute("SET search_path TO %s", [settings.DB_SCHEMA])
#     cursor_obj.close()

