from datetime import datetime
from typing import List
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Document(Base):
    __tablename__ = 'document'
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    rubrics: Mapped[List[str]] = mapped_column(JSON)
    text: Mapped[str]
    created_date: Mapped[datetime]
