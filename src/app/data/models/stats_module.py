from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class StatsModule(Base):
    __tablename__ = 'stats_modules'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(String(128))
    token: Mapped[str] = mapped_column(String(256))
