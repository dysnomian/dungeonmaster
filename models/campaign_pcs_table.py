from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


campaign_pcs_table = Table(
    "campaign_pcs",
    Base.metadata,
    Column("campaign_id", ForeignKey("campaigns.id"), primary_key=True),
    Column("character_sheet_id", ForeignKey("character_sheets.id"), primary_key=True),
)
