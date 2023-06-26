from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db


class SoldierStones(db.Model):
    __tablename__ = "soldier_stones"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), nullable=False)

    aphoto_url: orm.Mapped[str] = orm.mapped_column(sa.String(256))

    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )
    date: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime, nullable=False)

    sender_name: orm.Mapped[str] = orm.mapped_column(sa.String(256))

    sender_email: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=False)
