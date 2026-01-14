from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from database import Base
from app.data.types import CreatedAt, ID


class Meeting(Base):
    __tablename__ = 'meetings'

    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    text_id: Mapped[str] = mapped_column(String(128), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    whiteboard_id: Mapped[int] = mapped_column(nullable=True)
    analytics: Mapped[dict[str, any] | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[CreatedAt]
