import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin


class SoldierRank(db.Model, ModelMixin):
    __tablename__ = "soldier_ranks"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    rank_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("ranks.id"),
        nullable=False,
    )
    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )

    @property
    def name(self):
        return self.rank.name
