from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port="5433",
    dbname="Mashshop",
    user="postgres",
    password="1234",
    options="-c client_encoding=latin-1"
)


engine = create_engine("postgresql://postgres:1234@localhost:5433/Mashshop")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()