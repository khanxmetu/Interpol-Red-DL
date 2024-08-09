import sys, os
sys.path.append(os.getcwd())

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from notice_saver.offense_classifier import BasicOffenseClassifier, OffenseClassifier
from notice_saver.models import Base
from notice_saver.notice_saver import NoticeSaver
from notice_saver.repositories import (
    ArrestWarrantRepository,
    OffenseTypeRepository,
    CountryRepository,
    EyeColorRepository,
    HairColorRepository,
    SexRepository,
    LanguageRepository,
    NoticeRepository,
)
from notice_saver.repositories_manager import RepositoriesManager

db_connection_url = URL.create(
    drivername=os.environ["DB_DRIVER"],
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASS"],
    host=os.environ["DB_HOST"],
    port=int(os.environ["DB_PORT"]),
    database=os.environ["DB_NAME"],
)
engine = create_engine(db_connection_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


hair_color_repo = HairColorRepository(session)
eye_color_repo = EyeColorRepository(session)
country_repo = CountryRepository(session)
sex_repo = SexRepository(session)
language_repo = LanguageRepository(session)
notice_repo = NoticeRepository(session)
offense_type_repo = OffenseTypeRepository(session)
arrest_warrant_repo = ArrestWarrantRepository(session)
repositories_manager = RepositoriesManager(
    hair_color_repository=hair_color_repo,
    eye_color_repository=eye_color_repo,
    country_repository=country_repo,
    sex_repository=sex_repo,
    language_repository=language_repo,
    notice_repository=notice_repo,
    offense_type_repository=offense_type_repo,
)
repositories_manager.preload_data()

offense_classifier = BasicOffenseClassifier(offense_type_repository=offense_type_repo)


def main():
    assigned = 0
    max_offense_types = 0
    max_offense_types_aw = None
    arrest_warrant_objs = arrest_warrant_repo.get_all()
    print(arrest_warrant_objs)
    for arrest_warrant in arrest_warrant_objs:
        arrest_warrant.offense_types = offense_classifier.classify(
            arrest_warrant.charge or arrest_warrant.charge_translation or ""
        )
        if arrest_warrant.offense_types:
            assigned += 1
            if len(arrest_warrant.offense_types) > max_offense_types:
                max_offense_types = len(arrest_warrant.offense_types)
                max_offense_types_aw = arrest_warrant
        arrest_warrant_repo.save(arrest_warrant)
        print(arrest_warrant.id, "saved")

    total = len(arrest_warrant_objs)
    print(f"Arrest Warrant ID: {max_offense_types_aw.id} has highest number of offense type tags: {max_offense_types}")
    print(f"Classified {assigned} out of {total} arrest warrants")


main()
