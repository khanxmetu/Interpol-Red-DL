import json
from notice_saver.models import (
    _OffenseType,
    _Country,
    _EyeColor,
    _HairColor,
    _Language,
    _Sex,
)
from notice_saver.repositories import (
    OffenseTypeRepository,
    CountryRepository,
    EyeColorRepository,
    HairColorRepository,
    LanguageRepository,
    NoticeRepository,
    SexRepository,
)

PRELOAD_DATA_DIR = "notice_saver/preload_data"


class RepositoriesManager:
    def __init__(
        self,
        hair_color_repository: HairColorRepository,
        eye_color_repository: EyeColorRepository,
        language_repository: LanguageRepository,
        sex_repository: SexRepository,
        country_repository: CountryRepository,
        offense_type_repository: OffenseTypeRepository,
        notice_repository: NoticeRepository,
    ):
        self.hair_color_repository = hair_color_repository
        self.eye_color_repository = eye_color_repository
        self.language_repository = language_repository
        self.sex_repository = sex_repository
        self.country_repository = country_repository
        self.notice_repository = notice_repository
        self.offense_type_repository = offense_type_repository

    def preload_data(self):
        """
        Preloads the data for restricted tables
        which are intended to be used for read-only purposes only
        """
        with open(PRELOAD_DATA_DIR + "/hair_color_codes.json") as f:
            hair_color_data = json.load(f)
        self._preload_data_pairs_into_repository(
            hair_color_data, self.hair_color_repository, _HairColor
        )

        with open(PRELOAD_DATA_DIR + "/eye_color_codes.json") as f:
            eye_color_data = json.load(f)
        self._preload_data_pairs_into_repository(
            eye_color_data, self.eye_color_repository, _EyeColor
        )

        with open(PRELOAD_DATA_DIR + "/language_codes.json", encoding="utf-8") as f:
            language_data = json.load(f)
        self._preload_data_pairs_into_repository(
            language_data, self.language_repository, _Language
        )

        with open(PRELOAD_DATA_DIR + "/sex_codes.json") as f:
            sex_data = json.load(f)
        self._preload_data_pairs_into_repository(sex_data, self.sex_repository, _Sex)

        with open(PRELOAD_DATA_DIR + "/offense_types.json") as f:
            offense_type_data = json.load(f)
        self._preload_offense_type_data(offense_type_data)

        with open(PRELOAD_DATA_DIR + "/country_codes.json", encoding="utf-8") as f:
            country_data = json.load(f)
        self._preload_country_data(country_data)

    def _preload_offense_type_data(self, offense_type_data: dict) -> None:
        for id, value in offense_type_data.items():
            id = int(id)
            offense_type = _OffenseType(id=id, value=value)
            self.offense_type_repository._register_object(offense_type)

    def _preload_country_data(self, country_data: dict) -> None:
        for id, details in country_data.items():
            country = _Country(
                id=id, iso_a3=details["iso_a3"], value=details["full_name"]
            )
            self.country_repository._register_object(country)

    def _preload_data_pairs_into_repository(
        self, data: dict[str, str], repo_obj, model_class
    ) -> None:
        for id, value in data.items():
            obj = model_class(id=id, value=value)
            repo_obj._register_object(obj)
