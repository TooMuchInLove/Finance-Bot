from datetime import datetime
from uuid import uuid4

from sqlalchemy import ForeignKey, String, BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.schema import CheckConstraint

from api.infra.models.base import BaseModel


class AccountModel(BaseModel):
    __tablename__ = "account"

    id: Mapped[UUID] = mapped_column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    telegram_user_id: Mapped[int] = mapped_column(
        "telegram_user_id",
        BigInteger,
        unique=True,
        nullable=False,
    )
    telegram_username: Mapped[str] = mapped_column(
        "telegram_username",
        String,
        unique=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    categories: Mapped[list["CategoryModel"]] = relationship(
        "CategoryModel",
        back_populates="account",
        cascade="all, delete-orphan",
        lazy="selectin",
        single_parent=True,
    )


class CategoryModel(BaseModel):
    __tablename__ = "category"

    account_id: Mapped[UUID] = mapped_column(
        "account_id",
        UUID(as_uuid=True),
        ForeignKey("account.id"),
        primary_key=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        "name",
        String(100),
        primary_key=True,
        nullable=False,
        info={"constraints": [CheckConstraint("LENGTH(name) >= 3")]},
    )
    sub_name: Mapped[str] = mapped_column(
        "sub_name",
        String(100),
        primary_key=True,
        nullable=False,
        info={"constraints": [CheckConstraint("LENGTH(name) >= 3")]},
    )
    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    account: Mapped["AccountModel"] = relationship(
        "AccountModel",
        back_populates="categories",
        # cascade="all, delete-orphan",
    )
