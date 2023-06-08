import sqlalchemy as sa
from sqlalchemy import orm

from app import schema as s
from app.database import db

from .soldier_award import SoldierAward
from .utils import ModelMixin


class Award(db.Model, ModelMixin):
    __tablename__ = "awards"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        nullable=False,
    )

    soldier_awards: orm.Mapped[SoldierAward] = orm.relationship(
        "SoldierAward",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "award",
            viewonly=True,
        ),
    )

    @property
    def json(self):
        data = s.Award.from_orm(self)
        return data.json(by_alias=True)
