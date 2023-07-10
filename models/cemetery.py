import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.hybrid import hybrid_property


from app.database import db
from app import schema as s

from .utils import generate_uuid, ModelMixin
from .cemetery_audio_tour import CemeteryAudioTour
from .soldier_dashboar_filter import SoldierDashboardFilter
from .soldier import Soldier


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

    amount_buried_soldiers_common: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, nullable=True
    )
    amount_buried_soldiers_jewish: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, nullable=True
    )
    amount_buried_soldiers_missing: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, nullable=True
    )

    war_id = orm.mapped_column(sa.ForeignKey("wars.id"), nullable=True)
    _war = orm.relationship("War", viewonly=True)

    @hybrid_property
    def war(self):
        return self._war.name

    @property
    def audio_tours(self):
        return [tour.aws_filepath for tour in self._audio_tours]

    _audio_tours: orm.Mapped[CemeteryAudioTour] = orm.relationship(
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

    @property
    def graves_coordinates(self):
        session = orm.object_session(self)
        graves_coordinates = session.execute(
            Soldier.select()
            .where(Soldier.cemetery_id == self.id)
            .where(Soldier.burial_location_latitude.isnot(None))
            .where(Soldier.burial_location_longitude.isnot(None))
        ).scalars()
        return list(graves_coordinates)

    @property
    def soldies_headstones_changed(self):
        session = orm.object_session(self)
        graves_coordinates = session.execute(
            Soldier.select()
            .where(Soldier.cemetery_id == self.id)
            .where(Soldier.is_headstone_changed.is_(True))
        ).scalars()
        return list(graves_coordinates)

    @property
    def filtered_soldiers(self):
        session = orm.object_session(self)
        soldier_filter: SoldierDashboardFilter | None = session.execute(
            SoldierDashboardFilter.select()
        ).scalar()

        if not soldier_filter:
            return None

        soldier_filter_expressions = Soldier.generate_filter(soldier_filter)
        if not soldier_filter_expressions:
            return None

        soldiers = session.execute(
            Soldier.select()
            .where(*soldier_filter_expressions, Soldier.cemetery_id == self.id)
            .limit(soldier_filter.soldiers_amount)
        ).scalars()
        return s.SoldiersFiltered(title=soldier_filter.title, soldiers=list(soldiers))
