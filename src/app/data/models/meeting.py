from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base
from app.data.types import CreatedAt, ID


class Meeting(Base):
    __tablename__ = 'meetings'

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    text_id: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    whiteboard_id: Mapped[int] = mapped_column(nullable=True)
    analytics: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[CreatedAt]
