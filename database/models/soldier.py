import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm

from database import db

from api.utils import generate_uuid


class Soldier(db.Model):
    __tablename__ = "soldiers"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
        index=True,
    )

    # TODO cemetery_id = Column(Integer, ForeignKey('cemetery.id'))
    # TODO pic = Column(String(124), nullable=True)

    description: orm.Mapped[str] = orm.mapped_column(sa.String(254))
    address: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    rank: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    first_name: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    last_name: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    birth_date: orm.Mapped[dt.date] = orm.mapped_column(sa.Date)
    death_date: orm.Mapped[dt.date] = orm.mapped_column(sa.Date)
    birth_location: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    service_number: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    service_branch: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    service_state: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    assignment: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    awards: orm.Mapped[str] = orm.mapped_column(sa.String(256))
    position: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    service_card: orm.Mapped[str] = orm.mapped_column(sa.String(124))

    death_circumstance: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    initial_burial_location: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    final_burial_location: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    tablet_of_missing: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    telegram_pdf: orm.Mapped[str] = orm.mapped_column(sa.String(124))
    change_ceremony_link: orm.Mapped[str] = orm.mapped_column(sa.String(124))


class SoldierMessage(db.Model):
    __tablename__ = "soldier_messages"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
        index=True,
    )

    message_text: orm.Mapped[str] = orm.mapped_column(sa.String(256))
    reply_email: orm.Mapped[str] = orm.mapped_column(sa.String(124))

    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"), nullable=False
    )


class SoldierAudio(db.Model):
    ...