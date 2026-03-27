from datetime import datetime
from uuid import uuid4

from sqlalchemy import String, BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from api.infra.models.base import BaseModel


class AccountModel(BaseModel):
    __tablename__ = "account"

    id: Mapped[UUID] = mapped_column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )
    telegram_user_id: Mapped[int] = mapped_column(
        "telegram_user_id",
        BigInteger,
        unique=True,
        nullable=False
    )
    telegram_username: Mapped[str] = mapped_column(
        "telegram_username",
        String,
        unique=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
