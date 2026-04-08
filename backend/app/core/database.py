from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine, expire_on_commit=False)
class Base(DeclarativeBase):
    pass


def get_db():
    """This function is a generator that provides a database session to the caller.
    It creates a new session, yields it to the caller, and ensures that the session is properly closed after use.
    If any SQLAlchemyError occurs during the session, it rolls back the transaction and raises the error.

    Yields:
        _type_: A SQLAlchemy session object that can be used to interact with the database.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError:
        db.rollback()
        raise
    finally:
        db.close()
