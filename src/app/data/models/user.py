from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from app.data.types import ID


class User(Base):
    __tablename__ = 'users'

    id: Mapped[ID]
    internal_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(128))
    group: Mapped[str] = mapped_column(String(32))
    position: Mapped[str] = mapped_column(String(64))
    role: Mapped[str] = mapped_column(String(32))
