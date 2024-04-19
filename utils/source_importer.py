import json

from db import session, engine
from models.base import Base
from models.source import Source

Base.metadata.create_all(engine)

IMPORT_PATH = "import_data/sources.json"


def import_sources() -> None:
    sources = []
    try:
        with open(IMPORT_PATH, "r", encoding="utf-8") as f:
            sources = json.load(f)
    except FileNotFoundError:
        print(f"Error: file {IMPORT_PATH} not found")
        return

    combined_sources = sources.get("book", []) + sources.get("adventure", [])
    print(f"Importing {len(combined_sources)} sources from {IMPORT_PATH}")

    for source in combined_sources:
        try:
            print("Source: ", source.get("name"))
            source_obj = Source(
                name=source.get("name"),
                abbreviation=source.get("id"),
                published=source.get("publication"),
                author=source.get("author"),
                group=source.get("group"),
            )
            session.add(source_obj)
            session.commit()
        except Exception as e:
            print(
                f"Error importing source {source.get('name')} from {IMPORT_PATH}: {e}"
            )
            session.rollback()
