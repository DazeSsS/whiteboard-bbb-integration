from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from app.data.types import CreatedAt, ID


class Meeting(Base):
    __tablename__ = 'meetings'

    id: Mapped[ID]
    string_id: Mapped[str] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(128))
    analytics: Mapped[str] = mapped_column()
    date: Mapped[CreatedAt]
