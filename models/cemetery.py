import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property


from app.database import db
from app import schema as s

from .utils import generate_uuid, ModelMixin
from .cemetery_audio_tour import CemeteryAudioTour


class Cemetery(db.Model, ModelMixin):
    __tablename__ = "cemeteries"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
        index=True,
    )
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(64),
        nullable=False,
        unique=True,
        index=True,
    )
    location: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)

    latitude: orm.Mapped[float] = orm.mapped_column(sa.Float, nullable=True)
    longitude: orm.Mapped[float] = orm.mapped_column(sa.Float, nullable=True)

    phone: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String(320), nullable=True)
    web_url: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=True)

    superintendent: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)

    war_id = orm.mapped_column(sa.ForeignKey("wars.id"), nullable=True)
    _war = orm.relationship("War", viewonly=True)

    @hybrid_property
    def war(self):
        return self._war.name

    audio_tours: orm.Mapped[CemeteryAudioTour] = orm.relationship(
        "CemeteryAudioTour",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "cemetery",
            viewonly=True,
        ),
    )

    @property
    def json(self):
        data = s.Cemetery.from_orm(self)
        return data.json(by_alias=True)
