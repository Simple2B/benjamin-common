import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db

class War(db.Model):
    __tablename__ = "wars"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(64))
