import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from .utils import ModelMixin


class SoldierStateEnteredFrom(db.Model, ModelMixin):
    __tablename__ = "soldier_states_entered_from"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    state_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("states.id"),
        nullable=False,
    )
    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )

    @property
    def name(self):
        return self.state.name
