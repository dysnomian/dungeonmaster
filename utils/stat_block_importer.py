import os
import json

from db import session, engine
from models.base import Base
from models.stat_block import StatBlock
from utils.logging import logger
from utils.importers import IMPORT_PATH, source_dict

Base.metadata.create_all(engine)


def import_stat_blocks(filename) -> None:
    stat_blocks = []
    logger.info("importing creature stat blocks from %filename")
    with open(filename, "r", encoding="utf-8") as f:
        stat_blocks = json.load(f).get("monster", [])

    # print the keys for all the stat blocks
    stat_block_keys = set()
    for stat_block in stat_blocks:
        stat_block_keys.update(stat_block.keys())
    logger.debug("stat_block_keys: %stat_block_keys")

    for stat_block in stat_blocks:
        try:
            ability_scores = {
                "STR": stat_block.get("str", 0),
                "DEX": stat_block.get("dex", 0),
                "CON": stat_block.get("con", 0),
                "INT": stat_block.get("int", 0),
                "WIS": stat_block.get("wis", 0),
                "CHA": stat_block.get("cha", 0),
            }

            saving_throw_bonuses = {
                "STR": stat_block.get("save", {}).get("str", 0),
                "DEX": stat_block.get("save", {}).get("dex", 0),
                "CON": stat_block.get("save", {}).get("con", 0),
                "INT": stat_block.get("save", {}).get("int", 0),
                "WIS": stat_block.get("save", {}).get("wis", 0),
                "CHA": stat_block.get("save", {}).get("cha", 0),
            }

            logger.debug("stat_block: %s", stat_block.get("name"))
            stat_block_obj = StatBlock(
                name=stat_block.get("name"),
                source_id=source_dict().get(stat_block.get("source")),
                source_page=stat_block.get("page"),
                srd=stat_block.get("srd"),
                sizes=stat_block.get("size"),
                creature_type=stat_block.get("type"),
                alignments=stat_block.get("alignment"),
                ac=stat_block.get("ac"),
                hp=stat_block.get("hp"),
                speed=stat_block.get("speed"),
                ability_scores=ability_scores,
                saving_throw_bonuses=saving_throw_bonuses,
                skills=stat_block.get("skill"),
                senses=stat_block.get("senses"),
                languages=stat_block.get("languages"),
                cr=stat_block.get("cr"),
                traits=stat_block.get("trait"),
                actions=stat_block.get("action"),
                reactions=stat_block.get("reaction"),
                legendary_actions=stat_block.get("legendary"),
                environments=stat_block.get("environment"),
                condition_immunities=stat_block.get("conditionImmune"),
                immunities=stat_block.get("immune"),
            )
            session.add(stat_block_obj)
            session.commit()
        except Exception as e:
            logger.error(
                "Error importing stat block %s from %s: %s",
                stat_block.get("name"),
                filename,
                e,
            )
            session.rollback()


def import_all_stat_blocks() -> None:
    # for each file in the import_data directory, call import_stat_blocks
    # get a list of all files in the directory with "bestiary.json" in the name
    import_files = [f for f in os.listdir(IMPORT_PATH) if "bestiary.json" in f]
    logger.info("Found %d files to import: %s", len(import_files), import_files)
    for import_file in import_files:
        import_stat_blocks(IMPORT_PATH + import_file)
