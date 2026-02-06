from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.enums.user import UserRole
from database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=False,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(128))
    role: Mapped[UserRole] = mapped_column(
        String(32),
        server_default=UserRole.VIEWER,
    )
    token: Mapped[str] = mapped_column(String(256))
