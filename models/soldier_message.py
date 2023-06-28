import enum
import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db


class SoldierMessageType(enum.Enum):
    FAMILY = 1
    OB = 2
    UNASSIGNED = 3


class SoldierMessage(db.Model):
    __tablename__ = "soldier_messages"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    message_text: orm.Mapped[str] = orm.mapped_column(sa.String(512))
    message_type: orm.Mapped[SoldierMessageType] = orm.mapped_column(
        sa.Enum(SoldierMessageType), nullable=False
    )

    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )
