from datetime import datetime
from typing import Optional
import pandas as pd
from sqlalchemy.orm import aliased
from sqlalchemy.sql import exists, select
from sqlalchemy.orm import Session, joinedload
from models import notice_nationality_association

from models import (
    _OffenseType,
    _Country,
    _EyeColor,
    _HairColor,
    _Language,
    _Sex,
    ArrestWarrant,
    Notice,
    arrest_warrant_offense_type_association,
)


class NoticeRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, notice_id: str) -> Optional[Notice]:
        return self._session.query(Notice).filter_by(id=notice_id).first()

    def already_exists(self, notice_id: str) -> bool:
        return self._session.query(exists().where(Notice.id == notice_id)).scalar()

    def save(self, new_notice: Notice) -> None:
        new_notice.last_fetched_date = datetime.utcnow()
        try:
            self._session.merge(new_notice)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

    def get_notices_minimal_data_as_dataframe(self) -> pd.DataFrame:
        """Returns pd.DataFrame from columns id, name, forename"""
        statment = self._session.query(
            Notice.id, Notice.name, Notice.forename
        ).statement
        with self._session.connection() as connection:
            return pd.read_sql(statment, connection, index_col="id")

    def get_count(self) -> int:
        return self._session.query(Notice).count()


class ArrestWarrantRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, arrest_warrant_id: str) -> Optional[ArrestWarrant]:
        return (
            self._session.query(ArrestWarrant).filter_by(id=arrest_warrant_id).first()
        )

    def get_all(self) -> list[ArrestWarrant]:
        return self._session.query(ArrestWarrant).all()

    def get_classified_count(self) -> int:
        return (
            self._session.query(ArrestWarrant)
            .join(ArrestWarrant.offense_types)
            .group_by(ArrestWarrant.id)
            .count()
        )

    def get_count(self) -> int:
        return self._session.query(ArrestWarrant).count()

    def get_detailed_arrest_warrants_as_dataframe(self) -> int:
        IssuingCountry = aliased(_Country)
        Nationality = aliased(_Country)
        statement = (
            self._session.query(
                ArrestWarrant,
                _OffenseType.value.label("offense_type"),
                Notice,
                IssuingCountry.iso_a3.label("issuing_country_iso_a3"),
                IssuingCountry.value.label("issuing_country_name"),
                Nationality.iso_a3.label("nationality_iso_a3"),
                Nationality.value.label("nationality_name"),
            )
            .outerjoin(
                arrest_warrant_offense_type_association,
                ArrestWarrant.id
                == arrest_warrant_offense_type_association.c.arrest_warrant_id,
            )
            .outerjoin(
                _OffenseType,
                _OffenseType.id
                == arrest_warrant_offense_type_association.c.offense_type_id,
            )
            .outerjoin(IssuingCountry, IssuingCountry.id == ArrestWarrant.issuing_country_id)
            .outerjoin(Notice, Notice.id == ArrestWarrant.notice_id)
            .outerjoin(
                notice_nationality_association,
                Notice.id == notice_nationality_association.c.notice_id,
            )
            .outerjoin(
                Nationality,
                Nationality.id == notice_nationality_association.c.nationality_id,
            )
            .statement
        )

        with self._session.connection() as connection:
            return pd.read_sql(statement, connection)

class OffenseTypeRepository:
    def __init__(self, session: Session):
        self._session = session
        self._map = {}

    def get_by_id(self, offense_type_id: str | int) -> Optional[_OffenseType]:
        offense_type_id = int(offense_type_id)
        return self._map.get(offense_type_id)

    def _register_object(self, offense_type: _OffenseType) -> None:
        self._map[offense_type.id] = self._session.merge(offense_type)
        self._session.commit()


class HairColorRepository:
    def __init__(self, session: Session):
        self._session = session
        self._map = {}

    def get_by_id(self, hair_color_id: str) -> Optional[_HairColor]:
        return self._map.get(hair_color_id)

    def _register_object(self, hair_color: _HairColor) -> None:
        self._map[hair_color.id] = self._session.merge(hair_color)
        self._session.commit()


class EyeColorRepository:
    def __init__(self, session: Session):
        self._session = session
        self._map = {}

    def get_by_id(self, eye_color_id: str) -> Optional[_EyeColor]:
        return self._map.get(eye_color_id)

    def _register_object(self, eye_color: _EyeColor) -> None:
        self._map[eye_color.id] = self._session.merge(eye_color)
        self._session.commit()


class CountryRepository:
    def __init__(self, session: Session):
        self._session = session
        self._map = {}

    def get_by_id(self, country_id: str) -> Optional[_Country]:
        return self._map.get(country_id)

    def _register_object(self, country: _Country) -> None:
        self._map[country.id] = self._session.merge(country)
        self._session.commit()


class LanguageRepository:
    def __init__(self, session: Session):
        self._session = session
        self._map = {}

    def get_by_id(self, language_id: str) -> Optional[_Language]:
        return self._map.get(language_id)

    def _register_object(self, language: _Language) -> None:
        self._map[language.id] = self._session.merge(language)
        self._session.commit()


class SexRepository:
    def __init__(self, session: Session):
        self._session = session
        self._map = {}

    def get_by_id(self, sex_id: str) -> Optional[_Sex]:
        return self._map.get(sex_id)

    def _register_object(self, sex: _Sex) -> None:
        self._map[sex.id] = self._session.merge(sex)
        self._session.commit()
