from sqlalchemy import String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import TIMESTAMP

from models.base import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    abbreviation: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    published: Mapped[DateTime] = mapped_column(TIMESTAMP, nullable=True)
    author: Mapped[str] = mapped_column(String(255), nullable=True)
    group: Mapped[str] = mapped_column(String(255), nullable=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=True)
