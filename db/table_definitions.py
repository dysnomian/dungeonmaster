from sqlalchemy import Column, Integer, String, Boolean, Identity, Table, text
from sqlalchemy import MetaData

from db import engine

metadata = MetaData()

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.fetchone())


Base.metadata.create_all(engine)
