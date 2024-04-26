from sqlalchemy import Column, ForeignKey, Table

from models.base import Base

campaign_npcs_table = Table(
    "campaign_npcs",
    Base.metadata,
    Column("campaign_id", ForeignKey("campaigns.id"), primary_key=True),
    Column("npc_id", ForeignKey("npcs.id"), primary_key=True),
)
