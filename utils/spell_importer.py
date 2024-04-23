import os
import json

from db import session, engine
from models.base import Base
from models.spell import Spell
from utils.importers import IMPORT_PATH, source_dict

Base.metadata.create_all(engine)


def import_spells(filename: str) -> None:
    spells = []
    print(f"Importing spells from {filename}")
    with open(filename, "r", encoding="utf-8") as f:
        spells = json.load(f).get("spell", [])

    for spell in spells:
        try:
            print(f"Spell: {spell.get('name')}")
            spell_obj = Spell(
                name=spell.get("name"),
                source_id=source_dict().get(spell.get("source")),
                source_page=spell.get("page"),
                range=spell.get("range"),
                time=spell.get("time"),
                components=spell.get("components"),
                duration=spell.get("duration"),
                meta=spell.get("meta"),
                entries=spell.get("entries"),
                scaling_level_dice=spell.get("scalingLevelDice"),
                damage_inflict=spell.get("damageInflict"),
                saving_throw=spell.get("savingThrow"),
                misc_tags=spell.get("miscTags"),
                area_tags=spell.get("areaTags"),
            )
            session.add(spell_obj)
            session.commit()
        except Exception as e:
            print(f"Error importing spell {spell.get('name')} from {filename}: {e}")
            session.rollback()


def import_all_spells() -> None:
    # for each file in the import_data directory, call import_spells
    # get a list of all files in the directory with "-spells.json" in the name
    import_files = [f for f in os.listdir(IMPORT_PATH) if "-spells.json" in f]
    print(f"Found {len(import_files)} files to import: {import_files}")
    for import_file in import_files:
        import_spells(IMPORT_PATH + import_file)
