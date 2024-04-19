import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine.url import URL

environment = os.getenv("DUNGEONMASTER_ENV", "dev")

url = URL.create(
    drivername="postgresql",
    username=f"dungeonmaster_{environment}",
    host=os.getenv("DUNGEONMASTER_DB_HOST", "localhost"),
    database=f"dungeonmaster_{environment}",
)

engine = create_engine(url, echo=True)
session = Session(engine)
