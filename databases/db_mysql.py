# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session

# DB_MYSQL_CONNECTION_STRING = "mysql+pymysql://root:root@localhost:3306/my-website"

# engine = create_engine(DB_MYSQL_CONNECTION_STRING, echo=True, future=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db_session():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# databases.py

from sqlmodel import SQLModel, create_engine, Session

DB_MYSQL_CONNECTION_STRING = "mysql+pymysql://root:root@localhost:3306/my-website"

# Use SQLModel's engine
engine = create_engine(DB_MYSQL_CONNECTION_STRING, echo=True)

# Dependency injection for FastAPI
def get_db_session():
    with Session(engine) as session:
        yield session

