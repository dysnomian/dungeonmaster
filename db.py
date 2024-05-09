import os
import psycopg2

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine.url import URL


environment = os.getenv("DUNGEONMASTER_ENV", "dev")
host = os.getenv("DUNGEONMASTER_DB_HOST", "localhost")
username = f"dungeonmaster_{environment}"
password = os.getenv("DUNGEONMASTER_DB_PASSWORD", "password")
database_name = f"dungeonmaster_{environment}"


url = URL.create(
    drivername="postgresql",
    username=username,
    host=host,
    database=database_name,
)

engine = create_engine(url)
session = Session(engine)

conn = psycopg2.connect(
    host=host,
    database=database_name,
    user=username,
    password=password
)

cursor = conn.cursor()
