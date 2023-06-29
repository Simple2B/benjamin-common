import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin


class SoldierPosition(db.Model, ModelMixin):
    __tablename__ = "soldier_positions"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    position_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("positions.id"),
        nullable=False,
    )
    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )

    @property
    def name(self):
        return self.position.name
