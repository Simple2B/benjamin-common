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


class Cemetery(db.Model):
    __tablename__ = "cemeteries"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
        index=True,
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(254), nullable=True)
    location: orm.Mapped[str] = orm.mapped_column(sa.String(254), nullable=True)

    latitude: orm.Mapped[float] = orm.mapped_column(sa.Float, nullable=True)
    longitude: orm.Mapped[float] = orm.mapped_column(sa.Float, nullable=True)

    phone: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String(320), nullable=True)
    url_path: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)

    superintendent: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)
    war: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)

    autdio_tours: orm.Mapped[CemeteryAudioTour] = orm.relationship(
        "CemeteryAudioTour",
        cascade="all, delete",
        lazy="dynamic",
        backref=orm.backref(
            "cemetery",
            viewonly=True,
        ),
    )
