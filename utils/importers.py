from typing import TYPE_CHECKING

from sqlalchemy.sql import select
from db import session

from models.source import Source

IMPORT_PATH = "import_data/"


def source_dict():
    stmt = select(Source)
    sources = session.execute(stmt).scalars().all()
    return {source.abbreviation: source.id for source in sources}
