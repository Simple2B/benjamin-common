import sqlalchemy as sa
from sqlalchemy import orm

from app import schema as s
from app.database import db

from .soldier_position import SoldierPosition
from .utils import ModelMixin


class Position(db.Model, ModelMixin):
    __tablename__ = "positions"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        nullable=False,
    )

    soldier_positions: orm.Mapped[SoldierPosition] = orm.relationship(
        "SoldierPosition",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "position",
            viewonly=True,
        ),
    )

    @property
    def json(self):
        data = s.Position.from_orm(self)
        return data.json(by_alias=True)
