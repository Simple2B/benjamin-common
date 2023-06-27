from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import orm, func

from app.database import db
from .utils import generate_uuid


class SoldierStone(db.Model):
    __tablename__ = "soldier_stones"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
        index=True,
    )
    photo_url: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=False)
    soldier_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("soldiers.id"),
        nullable=False,
    )
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime(timezone=True), server_default=func.now()
    )
    sender_name: orm.Mapped[str] = orm.mapped_column(sa.String(256))
    sender_email: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=False)
    is_verified: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)
