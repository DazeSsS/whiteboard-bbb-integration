from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Widget(Base):
    __tablename__ = 'widgets'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    whiteboard_id: Mapped[int] = mapped_column(nullable=False)
