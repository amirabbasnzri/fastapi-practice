from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager


DATABASE_URL = "postgresql+psycopg2://postgres:zdfjh.89s$@localhost:5432/mydb"
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    version = result.fetchone()
    print("PostgreSQL Version:", version[0])

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()  # commit
    except SQLAlchemyError as e:
        session.rollback()  # rollback
        print("error: ", e)
        raise
    finally:
        session.close()
