import sqlalchemy as sa
from sqlalchemy import orm

from app import schema as s
from app.database import db
from .utils import ModelMixin


class State(db.Model, ModelMixin):
    __tablename__ = "states"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        nullable=False,
    )

    @property
    def json(self):
        data = s.State.from_orm(self)
        return data.json(by_alias=True)
