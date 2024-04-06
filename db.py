from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import  load_dotenv
import os
#import psycopg2

"""connection = psycopg2.connect(
    host="localhost",
    port="5433",
    dbname="Mashshop",
    user="postgres",
    password="1234",
    options="-c client_encoding=latin-1"
)"""
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, connect_args={"options": "-c client_encoding=latin-1"})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()