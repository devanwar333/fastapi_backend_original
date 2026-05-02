import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel, text
from typing import Annotated
from fastapi import Depends

load_dotenv()
mysql_user = os.getenv("DATABASE_USER")
mysql_password = os.getenv("DATABASE_PASSWORD")
mysql_host = os.getenv("DATABASE_HOST")
mysql_port = os.getenv("DATABASE_PORT")
mysql_database_farm_name = os.getenv("DATABASE_CHICKEN_FARM")
mysql_database_cafe_name = os.getenv("DATABASE_CAFE_DAY")

mysql_url = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database_farm_name}"
mysql_database_cafe_name = f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database_cafe_name}"


engine_db_farm = create_engine(mysql_url , echo=True, pool_pre_ping=True, pool_recycle=3600)
engine_db_cafe = create_engine(mysql_database_cafe_name, echo=True, pool_pre_ping=True, pool_recycle=3600)

def get_session():
    with Session(engine_db_farm) as session:
        yield session

def get_session_cafe():
    with Session(engine_db_cafe) as session:
        yield session

def test_database_connection():
    try:
        with Session(engine_db_farm) as session:
            session.exec(text("SELECT 1"))
        print("Database farm connection successful!")

        with Session(engine_db_cafe) as session:
            session.exec(text("SELECT 1"))
        print("Database cafe connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")


SessionDB1 = Annotated[Session, Depends(get_session)]
SessionFarmDB = Annotated[Session, Depends(get_session)]
SessionCafeDB = Annotated[Session, Depends(get_session_cafe)]
