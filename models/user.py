import enum
import typing as t
import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm

from api.utils import generate_uuid
from api.hash_utils import make_hash
from app.database import db


class UserRoles(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(db.Model):
    __tablename__ = "users"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
        index=True,
    )
    email: orm.Mapped[str] = orm.mapped_column(
        sa.String(128), nullable=True, unique=True
    )
    username: orm.Mapped[str] = orm.mapped_column(
        sa.String(128), default="", unique=True
    )
    password_hash: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=True)
    user_role: orm.Mapped[UserRoles] = orm.mapped_column(
        sa.Enum(UserRoles), default=UserRoles.USER
    )
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(
        sa.DateTime, default=dt.datetime.utcnow
    )

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = make_hash(value)

    @classmethod
    def search(cls, db: orm.Session, login: str) -> t.Self:
        return (
            db.query(cls)
            .filter(
                sa.or_(
                    sa.func.lower(cls.username) == sa.func.lower(login),
                    sa.func.lower(cls.email) == sa.func.lower(login),
                )
            )
            .first()
        )

    def __repr__(self):
        return f"<{self.id}: {self.email}>"
