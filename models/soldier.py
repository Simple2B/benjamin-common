import datetime as dt
import sqlalchemy as sa
from sqlalchemy import orm

from app.database import db
from app import schema as s

from .soldier_award import SoldierAward
from .soldier_rank import SoldierRank
from .soldier_photo import SoldierPhoto
from .soldier_stones import SoldierStone
from .soldier_dashboar_filter import SoldierDashboardFilter
from .soldier_state_entered_service import SoldierStateEnteredFrom
from .soldier_military_unit import SoldierMilitaryUnit
from .guardian_of_heroes import GuardianOfHeroes
from .soldier_message import SoldierMessage, SoldierMessageType

from .utils import generate_uuid, ModelMixin


# TODO add place of death
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
    first_name: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=False)
    last_name: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=False)
    el_maleh: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=True)
    suffix: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=True)
    service_branch: orm.Mapped[str] = orm.mapped_column(sa.String(124), nullable=False)

    birth_date: orm.Mapped[dt.date] = orm.mapped_column(sa.Date, nullable=False)
    birth_location: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)

    death_date: orm.Mapped[dt.date] = orm.mapped_column(sa.Date, nullable=True)
    death_circumstance: orm.Mapped[str] = orm.mapped_column(
        sa.String(256), nullable=True
    )

    parents: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=True)
    is_headstone_changed: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean, default=False
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
    ranks: orm.Mapped[SoldierRank] = orm.relationship(
        "SoldierRank",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "soldier",
            viewonly=True,
        ),
    )
    states_entered_service_from: orm.Mapped[SoldierStateEnteredFrom] = orm.relationship(
        "SoldierStateEnteredFrom",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "soldier",
            viewonly=True,
        ),
    )
    military_units: orm.Mapped[SoldierMilitaryUnit] = orm.relationship(
        "SoldierMilitaryUnit",
        lazy="select",
        cascade="all, delete",
        backref=orm.backref(
            "soldier",
            viewonly=True,
        ),
    )

    stones: orm.Mapped[SoldierStone] = orm.relationship(
        "SoldierStone",
        lazy="select",
        cascade="all, delete",
    )
    verified_stones: orm.Mapped[SoldierStone] = orm.relationship(
        "SoldierStone",
        primaryjoin="and_(SoldierStone.soldier_id==Soldier.id, SoldierStone.is_verified==True)",
    )

    guardians_of_heroes: orm.Mapped[GuardianOfHeroes] = orm.relationship(
        "GuardianOfHeroes",
        lazy="select",
        cascade="all, delete",
    )

    @property
    def guardians(self):
        return [guard.name for guard in self.guardians_of_heroes]

    messages: orm.Mapped[SoldierMessage] = orm.relationship(
        "SoldierMessage",
        lazy="select",
        cascade="all, delete",
        backref="soldier",
    )

    @property
    def soldier_awards(self):
        return [award.name for award in self.awards]

    @property
    def soldier_states_entered_from(self):
        return [
            state_entered_service_from.name
            for state_entered_service_from in self.states_entered_service_from
        ]

    @property
    def soldier_ranks(self):
        return [rank.name for rank in self.ranks]

    @property
    def soldier_military_unit(self):
        return [unit.name for unit in self.military_units]

    @property
    def verified_messages(self):
        return list(
            filter(
                lambda message: message.message_type != SoldierMessageType.UNASSIGNED,
                self.messages,
            )
        )

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

    main_photo: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=True)
    hir_image: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=True)
    headstone_photo: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=True)

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

    assignment: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)
    position: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=True)

    jewish_servicemans_card: orm.Mapped[str] = orm.mapped_column(
        sa.String(256), nullable=True
    )
    ww_draft_card: orm.Mapped[str] = orm.mapped_column(sa.String(256), nullable=True)

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
