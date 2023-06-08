import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db


class SoldierPhoto(db.Model):
    __tablename__ = "soldier_photos"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    aws_filepath: orm.Mapped[str] = orm.mapped_column(sa.String(256))

    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )
