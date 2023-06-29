import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db

from .utils import ModelMixin


class SoldierMilitaryUnit(db.Model, ModelMixin):
    __tablename__ = "soldier_military_units"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    unit_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("military_units.id"),
        nullable=False,
    )
    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )

    @property
    def name(self):
        return self.unit.name
