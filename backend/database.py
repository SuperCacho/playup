import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

"""pool_pre_ping=true mantiene la conexion viva si supabase la duerme por inactividad"""
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


"""esta funcion nos va a servir para inyectar la bd en las rutas"""


def get_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
