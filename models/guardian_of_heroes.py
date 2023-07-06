import sqlalchemy as sa
from sqlalchemy import orm

from app import schema as s
from app.database import db

from .utils import ModelMixin


class GuardianOfHeroes(db.Model, ModelMixin):
    __tablename__ = "guardians_of_heroes"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(128),
        nullable=False,
    )

    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )

    @property
    def json(self):
        data = s.GuardianOfHeroes.from_orm(self)
        return data.json(by_alias=True)
