import json

from db import session, engine
from utils.logging import logger
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
        logger.error("Error: file %s not found", IMPORT_PATH)
        return

    combined_sources = sources.get("book", []) + sources.get("adventure", [])
    logger.info("Importing %d sources from %s", len(combined_sources), IMPORT_PATH)

    for source in combined_sources:
        try:
            logger.debug("source: %s", source.get("name"))
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
            logger.error(
                "Error importing source %s from %s: %s",
                source.get("name"),
                IMPORT_PATH,
                e,
            )
            session.rollback()
