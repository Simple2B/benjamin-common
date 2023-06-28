import sqlalchemy as sa
from sqlalchemy import orm

from app import schema as s
from app.database import db
from .utils import ModelMixin
from .soldier_state_entered_service import SoldierStateEnteredFrom


class State(db.Model, ModelMixin):
    __tablename__ = "states"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        nullable=False,
    )

    soldier_states_service_from: orm.Mapped[SoldierStateEnteredFrom] = orm.relationship(
        "SoldierStateEnteredFrom",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "state",
            viewonly=True,
        ),
    )

    @property
    def json(self):
        data = s.State.from_orm(self)
        return data.json(by_alias=True)
