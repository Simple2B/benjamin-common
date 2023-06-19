import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from app import schema as s

from .soldier_award import SoldierAward
from .soldier_photo import SoldierPhoto
from .soldier_dashboar_filter import SoldierDashboardFilter

from .utils import generate_uuid, ModelMixin


class Soldier(db.Model, ModelMixin):
    __tablename__ = "soldiers"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    uuid: orm.Mapped[str] = orm.mapped_column(
        sa.String(36),
        default=generate_uuid,
        index=True,
    )
    cemetery_id = orm.mapped_column(sa.ForeignKey("cemeteries.id"), nullable=True)

    service_number: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=False)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=False)
    service_branch: orm.Mapped[str] = orm.mapped_column(sa.String(124), nullable=False)

    birth_date: orm.Mapped[dt.date] = orm.mapped_column(sa.Date, nullable=False)
    birth_location: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)

    death_date: orm.Mapped[dt.date] = orm.mapped_column(sa.Date, nullable=True)
    death_circumstance: orm.Mapped[str] = orm.mapped_column(
        sa.String(256), nullable=True
    )

    awards: orm.Mapped[SoldierAward] = orm.relationship(
        "SoldierAward",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "soldier",
            viewonly=True,
        ),
    )

    @property
    def soldier_awards(self):
        return [award.name for award in self.awards]

    # AWS Files
    photos: orm.Mapped[SoldierPhoto] = orm.relationship(
        "SoldierPhoto",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "soldier",
            viewonly=True,
        ),
    )

    @property
    def photo_paths(self):
        return [photo.aws_filepath for photo in self.photos]

    soldier_audio_tour: orm.Mapped[str] = orm.mapped_column(
        sa.String(256),
        nullable=True,
    )

    kia_telegram: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=True)
    replacement_ceremony_video: orm.Mapped[str] = orm.mapped_column(
        sa.String(256), nullable=True
    )

    # Burial location
    burial_location_name: orm.Mapped[str] = orm.mapped_column(
        sa.String(124),
        nullable=True,
    )

    burial_location_latitude: orm.Mapped[str] = orm.mapped_column(
        sa.Float,
        nullable=True,
    )
    burial_location_longitude: orm.Mapped[str] = orm.mapped_column(
        sa.Float,
        nullable=True,
    )

    @property
    def burial_location(self):
        return {
            "name": self.burial_location_name,
            "longitude": self.burial_location_longitude,
            "latitude": self.burial_location_latitude,
        }

    state_entered_service_from: orm.Mapped[str] = orm.mapped_column(
        sa.String(64), nullable=True
    )
    assignment: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)
    position: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)

    jewish_servicemans_card: orm.Mapped[str] = orm.mapped_column(
        sa.String(256), nullable=True
    )

    initial_burial_location: orm.Mapped[str] = orm.mapped_column(
        sa.String(64), nullable=True
    )

    final_burial_location: orm.Mapped[str] = orm.mapped_column(
        sa.String(64), nullable=True
    )

    @property
    def soldier_title_photo(self):
        if self.photos:
            return self.photos[0].aws_filepath

        return None

    @property
    def json(self):
        data = s.Soldier.from_orm(self)
        return data.json(by_alias=True)

    @classmethod
    def generate_filter(
        cls, soldier_filter: SoldierDashboardFilter
    ) -> list[sa.BinaryExpression]:
        # sqlalchemy binary expressions list
        sa_expressions = []

        if soldier_filter.birth_date_from:
            sa_expressions.append(cls.birth_date > soldier_filter.birth_date_from)

        if soldier_filter.birth_date_to:
            sa_expressions.append(cls.birth_date < soldier_filter.birth_date_to)

        if soldier_filter.death_date_from:
            sa_expressions.append(cls.death_date > soldier_filter.birth_date_from)

        if soldier_filter.death_date_to:
            sa_expressions.append(cls.death_date < soldier_filter.death_date_to)

        if soldier_filter.birth_location:
            sa_expressions.append(cls.birth_location == soldier_filter.birth_location)

        return sa_expressions
