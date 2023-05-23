import enum
import typing as t
import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db, BaseUser
from app.logger import log
from app import schema as s

from .utils import generate_uuid, make_hash, hash_verify, ModelMixin


class User(db.Model, ModelMixin, BaseUser):
    __tablename__ = "users"

    class Role(enum.Enum):
        ADMIN = "admin"
        USER = "user"

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
    role: orm.Mapped[Role] = orm.mapped_column(sa.Enum(Role), default=Role.USER)
    created_at: orm.Mapped[dt.datetime] = orm.mapped_column(
        sa.DateTime, default=dt.datetime.utcnow
    )
    unique_id: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
    )
    reset_password_uid: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        default=generate_uuid,
    )

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = make_hash(value)

    @classmethod
    def search(cls, db: orm.Session, login: str) -> t.Self:
        query = cls.select().where(
            sa.func.lower(cls.username)
            == sa.func.lower(login) | sa.func.lower(cls.email)
            == sa.func.lower(login)
        )
        return db.scalar(query)

    @classmethod
    def authenticate(cls, user_id, password):
        query = cls.select().where(
            (sa.func.lower(cls.username) == sa.func.lower(user_id))
            | (sa.func.lower(cls.email) == sa.func.lower(user_id))
        )
        user: User = db.session.scalar(query)
        if not user:
            log(log.WARNING, "user:[%s] not found", user_id)

        if user is not None and hash_verify(password, user.password_hash):
            return user

    def reset_password(self):
        self.password_hash = ""
        self.reset_password_uid = generate_uuid()
        self.save()

    def __repr__(self):
        return f"<{self.id}: {self.email}>"

    @property
    def json(self):
        u = s.User.from_orm(self)
        return u.json()
