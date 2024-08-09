from datetime import datetime
from typing import Optional
from sqlalchemy import exists
from sqlalchemy.orm import Session

from notice_saver.models import (
    _OffenseType,
    _Country,
    _EyeColor,
    _HairColor,
    _Language,
    _Sex,
    ArrestWarrant,
    Notice,
)


class ArrestWarrantRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, arrest_warrant_id: str) -> Optional[ArrestWarrant]:
        return (
            self._session.query(ArrestWarrant).filter_by(id=arrest_warrant_id).first()
        )

    def get_all(self) -> list[ArrestWarrant]:
        return self._session.query(ArrestWarrant).all()

    def get_count(self) -> int:
        return self._session.query(ArrestWarrant).count()

    def save(self, arrest_warrant: ArrestWarrant) -> None:
        try:
            self._session.merge(arrest_warrant)
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e


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


class OffenseTypeRepository:
    def __init__(self, session: Session):
        self._session = session
        self._map_id_to_obj = {}
        self._map_value_to_obj = {}

    def get_by_id(self, offense_type_id: str | int) -> Optional[_OffenseType]:
        offense_type_id = int(offense_type_id)
        return self._map_id_to_obj.get(offense_type_id)

    def get_by_value(self, offense_type_value: str | int) -> Optional[_OffenseType]:
        return self._map_value_to_obj.get(offense_type_value)

    def get_all(self) -> list[_OffenseType]:
        return list(self._map_id_to_obj.values())

    def _register_object(self, offense_type: _OffenseType) -> None:
        obj = self._session.merge(offense_type)
        self._map_id_to_obj[offense_type.id] = obj
        self._map_value_to_obj[offense_type.value] = obj
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
