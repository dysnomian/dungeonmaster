import os
from pprint import pprint
import json

from sqlalchemy.sql import select

from db import session, engine
from models.base import Base
from models.race import Race, RaceVariants
from models.source import Source

Base.metadata.create_all(engine)

IMPORT_PATH = "import_data/"

# build a dict of all source ids with abbreviations
stmt = select(Source)
sources = session.execute(stmt).scalars().all()
source_dict = {source.abbreviation: source.id for source in sources}
source_publication_date_dict = {
    source.abbreviation: source.published for source in sources
}


def import_races(filename) -> None:
    print(f"Importing races from {filename}")
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
            print(f"Error sorting duplicate race names: {e}")
            pprint(race)

    # make sets for each duplicated race name
    duplicated_races = {}
    for name in duplicated_names:
        duplicated_races[name] = set()

    for race in combined_races:
        try:
            if race["name"] in duplicated_names:
                race["source_publication_date"] = source_publication_date_dict[
                    race["source"]
                ]
                duplicated_races[race["name"]].add(race)
        except Exception as e:
            print(f"Error appending source publication date {race["source"]} of {source_publication_date_dict[race["source"]]} to {race["name"]}: {e}")
            pprint(race)

    duplicates = {}
    for name in duplicated_names:
        duplicates[name] = []

    for race in combined_races:
        if race["name"] in duplicated_names:
            duplicates[race["name"]].append(race)

    for races in duplicates:
        races.sort(key=lambda x: x["published"], reverse=True)
        for race in races:
            if races.index(race) == 0:
                race["legacy"] = False
            else:
                race["legacy"] = True

    pprint(duplicates)
    return

    for race in all_races["race"]:
        try:
            print(f"race: {race.get('name')}")

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
                source_id=source_dict.get(race.get("source")),
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
            print(f"Error importing race {race.get('name')} from {filename}: {e}")
            session.rollback()

    for subrace in all_races["subrace"]:
        try:
            print(f"subrace: {subrace.get('name')}")

            # get parent id and source id
            parent_race_stmt = (
                select(Race)
                .filter(Race.source_id == source_dict.get(subrace.get("raceSource")))
                .filter(Race.name == subrace.get("raceName"))
            )
            parent_race = session.execute(parent_race_stmt).scalars().first()

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
                source_id=source_dict.get(subrace.get("source")),
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
        except Exception as e:
            print(f"Error importing subrace {subrace.get('name')} from {filename}: {e}")
            session.rollback()


def import_all_races() -> None:
    # for each file in the import_data directory, call import_races
    # get a list of all files in the directory with "races.json" in the name
    import_files = [f for f in os.listdir(IMPORT_PATH) if "races.json" in f]
    print(f"Found {len(import_files)} files to import: {import_files}")
    for import_file in import_files:
        import_races(IMPORT_PATH + import_file)
