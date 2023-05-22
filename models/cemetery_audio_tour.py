import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db

from .utils import generate_uuid


class CemeteryAudioTour(db.Model):
    __tablename__ = "cemetery_audio_tours"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
        index=True,
    )

    aws_filepath: orm.Mapped[str] = orm.mapped_column(sa.String(256))

    cemetery_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("cemeteries.id"), nullable=True
    )
