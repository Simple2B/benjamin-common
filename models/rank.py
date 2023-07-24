import sqlalchemy as sa
from sqlalchemy import orm

from app import schema as s
from app.database import db

from .soldier_rank import SoldierRank
from .utils import ModelMixin


class Rank(db.Model, ModelMixin):
    __tablename__ = "ranks"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
    )

    abbreviation: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
    )

    soldier_ranks: orm.Mapped[SoldierRank] = orm.relationship(
        "SoldierRank",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "rank",
            viewonly=True,
        ),
    )

    @property
    def json(self):
        data = s.Rank.from_orm(self)
        return data.json(by_alias=True)
