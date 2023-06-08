import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db

from .utils import ModelMixin


class SoldierAward(db.Model, ModelMixin):
    __tablename__ = "soldier_awards"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    award_id: orm.Mapped[str] = orm.mapped_column(
        sa.ForeignKey("awards.id"),
        nullable=False,
    )
    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )

    @property
    def name(self):
        return self.award.name
