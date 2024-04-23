import os
import json

from db import session, engine
from models.base import Base
from models.background import Background
from utils.importers import IMPORT_PATH, source_dict

Base.metadata.create_all(engine)


def import_backgrounds(filename) -> None:
    backgrounds = []
    print(f"Importing backgrounds from {filename}")
    with open(filename, "r", encoding="utf-8") as f:
        backgrounds = json.load(f).get("background", [])

    for background in backgrounds:
        try:
            print(f"background: {background.get('name')}")
            background_obj = Background(
                name=background.get("name"),
                source_id=source_dict().get(background.get("source")),
                source_page=background.get("page"),
                skill_proficiencies=background.get("skillProficiencies"),
                tool_proficiencies=background.get("toolProficiencies"),
                language_proficiencies=background.get("languageProficiencies"),
                starting_equipment=background.get("startingEquipment"),
                entries=background.get("entries"),
                additional_spells=background.get("additionalSpells"),
            )
            session.add(background_obj)
            session.commit()
        except Exception as e:
            print(
                f"Error importing background {background.get('name')} from {filename}: {e}"
            )
            session.rollback()


def import_all_backgrounds() -> None:
    # for each file in the import_data directory, call import_backgrounds
    # get a list of all files in the directory with "backgrounds.json" in the name
    import_files = [f for f in os.listdir(IMPORT_PATH) if "backgrounds.json" in f]
    print(f"Found {len(import_files)} files to import: {import_files}")
    for import_file in import_files:
        import_backgrounds(IMPORT_PATH + import_file)
