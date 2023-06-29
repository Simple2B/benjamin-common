import sqlalchemy as sa
from sqlalchemy import orm
from app.database import db

from app import schema as s
from .utils import ModelMixin
from .soldier_military_unit import SoldierMilitaryUnit


class MilitaryUnit(db.Model, ModelMixin):
    __tablename__ = "military_units"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=False)

    soldier_military_units: orm.Mapped[SoldierMilitaryUnit] = orm.relationship(
        "SoldierMilitaryUnit",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "unit",
            viewonly=True,
        ),
    )

    @property
    def json(self):
        data = s.MilitaryUnit.from_orm(self)
        return data.json(by_alias=True)
