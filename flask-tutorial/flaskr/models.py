from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    String, Text, Boolean,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from werkzeug.security import generate_password_hash, check_password_hash

from flaskr.db import db
from flaskr.forms import SignUpForm


# CREATE TABLE user_account (
#         id VARCHAR(36) NOT NULL,
#         mobile VARCHAR(32),
#         wechat_id VARCHAR(256),
#         email VARCHAR(30),
#         password TEXT,
#         PRIMARY KEY (id),
#         UNIQUE (mobile),
#         UNIQUE (wechat_id),
#         UNIQUE (email)
# )
class User(db.Model):
    __tablename__ = "user_account"

    @classmethod
    def from_email(cls, data: SignUpForm):
        return cls(
            id=uuid4(),
            email=data.email.data,
            password=generate_password_hash(data.password.data)
        )

    @classmethod
    def from_mobile(cls, mobile: str):
        return cls(
            id=uuid4(),
            mobile=mobile
        )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )
    mobile: Mapped[[Optional[str]]] = mapped_column(
        String(32),
        unique=True,
        nullable=True
    )
    wechat_id: Mapped[Optional[str]] = mapped_column(
        String(256),
        unique=True,
        nullable=True,
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(30),
        unique=True,
        nullable=True,
    )
    password: Mapped[Optional[str]] = mapped_column(
        Text(),
        nullable=True,
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean(),
        default=False,
    )
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    deleted_at: Mapped[Optional[datetime]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

    def is_password_matched(self, pw: str) -> bool:
        return check_password_hash(self.password, pw)

