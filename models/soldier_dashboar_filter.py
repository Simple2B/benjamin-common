import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from app import schema as s
from .utils import ModelMixin


class SoldierDashboardFilter(db.Model, ModelMixin):
    __tablename__ = "soldier_dashboard_filter"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=False)

    birth_date_from: orm.Mapped[dt.date] = orm.mapped_column(sa.Date, nullable=True)
    birth_date_to: orm.Mapped[dt.date] = orm.mapped_column(sa.Date, nullable=True)

    birth_location: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)

    death_date_from: orm.Mapped[dt.date] = orm.mapped_column(sa.Date, nullable=True)
    death_date_to: orm.Mapped[dt.date] = orm.mapped_column(sa.Date, nullable=True)

    soldiers_amount: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)

    @property
    def json(self):
        data = s.SoldierFilter.from_orm(self)
        return data.json(by_alias=True)
