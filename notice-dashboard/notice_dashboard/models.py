from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Unicode
from sqlalchemy import String, ForeignKey, create_engine, Column, Table
from datetime import date, datetime

from typing import Optional, List


class Base(DeclarativeBase):
    pass


class _Country(Base):
    """
    Note:
        This class is intended for internal use only and should not be instantiated directly by users.
        Please utilize one of the pre-existing instances available in the repository.
    """

    __tablename__ = "country"
    id: Mapped[str] = mapped_column(primary_key=True)
    iso_a3: Mapped[Optional[str]]
    value: Mapped[str] = Column(Unicode())


class _EyeColor(Base):
    """
    Note:
        This class is intended for internal use only and should not be instantiated directly by users.
        Please utilize one of the pre-existing instances available in the repository.
    """

    __tablename__ = "eye_color"
    id: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]


class _HairColor(Base):
    """
    Note:
        This class is intended for internal use only and should not be instantiated directly by users.
        Please utilize one of the pre-existing instances available in the repository.
    """

    __tablename__ = "hair_color"
    id: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]


class _Sex(Base):
    """
    Note:
        This class is intended for internal use only and should not be instantiated directly by users.
        Please utilize one of the pre-existing instances available in the repository.
    """

    __tablename__ = "sex"
    id: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str]


class _Language(Base):
    """
    Note:
        This class is intended for internal use only and should not be instantiated directly by users.
        Please utilize one of the pre-existing instances available in the repository.
    """

    __tablename__ = "language"
    id: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = Column(Unicode())


class _OffenseType(Base):
    """
    Note:
        This class is intended for internal use only and should not be instantiated directly by users.
        Please utilize one of the pre-existing instances available in the repository.
    """

    __tablename__ = "offense_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]


class ImageURL(Base):
    __tablename__ = "image_url"
    id: Mapped[int] = mapped_column(primary_key=True)
    notice_id: Mapped[str] = mapped_column(ForeignKey("notice.id"))
    original_url: Mapped[str] = mapped_column(String(200), unique=True)
    downloaded_url: Mapped[Optional[str]] = mapped_column(String(200), unique=True)
    notice: Mapped["Notice"] = relationship(back_populates="image_urls")


notice_nationality_association = Table(
    "notice_nationality_association",
    Base.metadata,
    Column("notice_id", ForeignKey("notice.id")),
    Column("nationality_id", ForeignKey("country.id")),
)

notice_eye_color_association = Table(
    "notice_eye_color_association",
    Base.metadata,
    Column("notice_id", ForeignKey("notice.id")),
    Column("eye_color_id", ForeignKey("eye_color.id")),
)

notice_hair_color_association = Table(
    "notice_hair_color_association",
    Base.metadata,
    Column("notice_id", ForeignKey("notice.id")),
    Column("hair_color_id", ForeignKey("hair_color.id")),
)

notice_language_spoken_association = Table(
    "notice_language_spoken_association",
    Base.metadata,
    Column("notice_id", ForeignKey("notice.id")),
    Column("language_id", ForeignKey("language.id")),
)
arrest_warrant_offense_type_association = Table(
    "arrest_warrant_offense_type_association",
    Base.metadata,
    Column("arrest_warrant_id", ForeignKey("arrest_warrant.id")),
    Column("offense_type_id", ForeignKey("offense_type.id")),
)


class ArrestWarrant(Base):
    __tablename__ = "arrest_warrant"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    notice_id: Mapped[str] = mapped_column(ForeignKey("notice.id"))
    charge: Mapped[Optional[str]] = mapped_column(String(2000))
    charge_translation: Mapped[Optional[str]] = mapped_column(String(2000))
    issuing_country_id: Mapped[Optional[str]] = mapped_column(ForeignKey("country.id"))
    issuing_country: Mapped[Optional[_Country]] = relationship()
    notice: Mapped["Notice"] = relationship(back_populates="arrest_warrants")
    offense_types: Mapped[List[_OffenseType]] = relationship(
        secondary=arrest_warrant_offense_type_association
    )


class Notice(Base):
    __tablename__ = "notice"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    forename: Mapped[Optional[str]] = mapped_column(String(100))
    date_of_birth: Mapped[Optional[date]]
    distinguishing_marks: Mapped[Optional[str]] = mapped_column(String(300))
    weight: Mapped[Optional[float]]
    height: Mapped[Optional[float]]
    place_of_birth: Mapped[Optional[str]] = mapped_column(String(200))
    country_of_birth_id: Mapped[Optional[str]] = mapped_column(ForeignKey("country.id"))
    country_of_birth: Mapped[Optional[_Country]] = relationship()
    sex_id: Mapped[Optional[str]] = mapped_column(ForeignKey("sex.id"))
    sex: Mapped[Optional[_Sex]] = relationship()
    nationalities: Mapped[Optional[List[_Country]]] = relationship(
        secondary=notice_nationality_association
    )
    eye_colors: Mapped[Optional[List[_EyeColor]]] = relationship(
        secondary=notice_eye_color_association
    )
    hair_colors: Mapped[Optional[List[_HairColor]]] = relationship(
        secondary=notice_hair_color_association
    )
    languages_spoken: Mapped[Optional[List[_Language]]] = relationship(
        secondary=notice_language_spoken_association
    )
    arrest_warrants: Mapped[Optional[List[ArrestWarrant]]] = relationship(
        back_populates="notice"
    )
    image_urls: Mapped[Optional[List[ImageURL]]] = relationship(back_populates="notice")
    url: Mapped[str] = mapped_column(String(100), unique=True)
    first_fetched_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_fetched_date: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )
