import os
import json

from sqlalchemy.sql import select, or_

from db import session, engine
from models.base import Base
from models.race import Race, RaceVariants

from utils.logging import logger
from utils.importers import IMPORT_PATH, source_dict

Base.metadata.create_all(engine)


def import_races(filename) -> None:
    logger.info("Importing races from %filename")
    logger.debug("source_dict: %source_dict")
    with open(filename, "r", encoding="utf-8") as f:
        all_races = json.load(f)

    combined_races = all_races.get("race", []) + all_races.get("subrace", [])

    # if there are multiple records with the same name, append the source abbreviation to the name
    # example: "Aarakocra" from "MPMM" becomes "Aarakocra (MPMM)"
    # First, find all the names. If they are duplicated, stash them in a set
    all_names = set()
    duplicated_names = set()
    for race in combined_races:
        try:
            if race["name"] in all_names:
                duplicated_names.add(race["name"])
            if race["name"] not in all_names:
                all_names.add(race["name"])
        except Exception as e:
            logger.error("Error sorting duplicate race name: %s, %s", str(race), str(e))

    for race in combined_races:
        try:
            if race["name"] in duplicated_names:
                race["original_name"] = race["name"]
                race["name"] = f"{race["name"]} ({race["source"]})"
        except Exception as e:
            logger.error("Error appending source to duplicate race name: %e")

    for race in all_races["race"]:
        try:
            logger.debug("race: %s", race.get("name"))

            senses = {}
            senses["darkvision"] = race.get("darkvision", 0)

            proficiencies = {}
            proficiencies["weapons_and_armor"] = race.get(
                "weaponsAndArmorProficiencies", []
            )
            proficiencies["weapons_and_armor"].append(race.get("armorProficiencies"))
            proficiencies["languages"] = race.get("languageProficiencies", [])
            proficiencies["skills"] = race.get("skillProficiencies", [])

            race_obj = Race(
                name=race["name"],
                source_id=source_dict().get(race["source"]),
                source_page=race.get("page"),
                size=race.get("size"),
                speed=race.get("speed"),
                ability_bonuses=race.get("abilityBonuses"),
                entries=race.get("entries"),
                additional_spells=race.get("additionalSpells"),
                age=race.get("age"),
                senses=senses,
                proficiencies=proficiencies,
                creature_types=race.get("creatureTypes"),
                trait_tags=race.get("traitTags"),
                condition_immunities=race.get("conditionImmunities"),
                resistances=race.get("resistances"),
                immunities=race.get("immunities"),
                vulnerabilities=race.get("vulnerabilities"),
            )
            session.add(race_obj)
            session.commit()
        except Exception as e:
            logger.error(
                "Error importing race %s from %s: %e",
                race.get("name"),
                filename,
                e,
            )
            session.rollback()

    for subrace in all_races["subrace"]:
        try:
            logger.info("subrace: %s", subrace.get("name"))

            # get parent id and source id
            parent_race_stmt = select(Race).filter(Race.source_id == source_dict().get(subrace.get("raceSource"))).filter(or_(Race.name == subrace.get("raceName"), Race.original_name == subrace.get("raceName")))
            parent_race = session.execute(parent_race_stmt).scalars().first()

            if not parent_race:
                raise Exception({"message":f"Parent race not found for race {subrace.get('raceName')} and source {subrace.get('raceSource')}"})
            if not parent_race.id:
                raise Exception({"message":f"Parent race id not found for race {subrace.get('raceName')} and source {subrace.get('raceSource')}"})
            if not parent_race.source_id:
                raise Exception({"message":f"Parent race source id not found for race {subrace.get('raceName')} and source {subrace.get('raceSource')}"})

            senses = {}
            senses["darkvision"] = subrace.get("darkvision", 0)

            proficiencies = {}
            proficiencies["weapons_and_armor"] = subrace.get(
                "weaponsAndArmorProficiencies", []
            )
            proficiencies["weapons_and_armor"].append(subrace.get("armorProficiencies"))
            proficiencies["languages"] = subrace.get("languageProficiencies", [])
            proficiencies["skills"] = subrace.get("skillProficiencies", [])

            subrace_obj = RaceVariants(
                name=subrace["name"],
                source_id=source_dict().get(subrace.get("source")),
                source_page=subrace.get("page"),
                size=subrace.get("size"),
                speed=subrace.get("speed"),
                ability_bonuses=subrace.get("ability"),
                entries=subrace.get("entries"),
                additional_spells=subrace.get("additionalSpells"),
                age=subrace.get("age"),
                senses=senses,
                proficiencies=proficiencies,
                creature_types=subrace.get("creatureTypes"),
                trait_tags=subrace.get("traitTags"),
                condition_immunities=subrace.get("conditionImmunities"),
                resistances=subrace.get("resistances"),
                immunities=subrace.get("immunities"),
                vulnerabilities=subrace.get("vulnerabilities"),
                parent_race_id=parent_race.id,
                parent_race_source_id=parent_race.source_id,
                alias=subrace.get("alias"),
                overwrite=subrace.get("overwrite"),
            )
            session.add(subrace_obj)
            session.commit()
        except KeyError as e:
            logger.error(
                "Error importing subrace from %s: %s\n%s",
                filename,
                str(subrace),
                str(e),
            )
            session.rollback()
        except Exception as e:
            logger.error(
                "Couldn't find subrace %s from %s: %s",
                subrace.get("name"),
                filename,
                e,
            )
            session.rollback()


def import_all_races() -> None:
    # for each file in the import_data directory, call import_races
    # get a list of all files in the directory with "races.json" in the name
    import_files = [f for f in os.listdir(IMPORT_PATH) if "races.json" in f]
    logger.info(
        "Found %d files to import: %s",
        len(import_files),
        import_files
    )
    for import_file in import_files:
        import_races(IMPORT_PATH + import_file)
