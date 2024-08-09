import json
import os

from minio import Minio
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from notice_saver.offense_classifier import BasicOffenseClassifier, OffenseClassifier
from notice_saver.image_downloader import ImageDownloader
from notice_saver.models import Base
from notice_saver.notice_saver import NoticeSaver
from notice_saver.rabbitmq_client import RabbitMQConsumer
from notice_saver.repositories import (
    OffenseTypeRepository,
    CountryRepository,
    EyeColorRepository,
    HairColorRepository,
    SexRepository,
    LanguageRepository,
    NoticeRepository,
)
from notice_saver.repositories_manager import RepositoriesManager
from notice_saver.notice_consumer import NoticeConsumer


def main() -> None:
    """
    Constructs the dependencies,
    binds `NoticeSaver.save_notice_from_dict` to `NoticeConsumer` and runs it
    """
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

    minio_client = Minio(
        endpoint=os.environ["MINIO_ADDRESS"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=False,
    )

    with open("config-data/headers.json") as f:
        interpol_request_headers = json.load(f)
    image_downloader = ImageDownloader(
        bucket_name=os.environ["MINIO_NOTICE_IMAGES_BUCKET"],
        public_base_url=os.environ["MINIO_PUBLIC_BASE_URL"],
        minio_client=minio_client,
        request_headers=interpol_request_headers,
    )

    notice_saver = NoticeSaver(
        repositories_manager=repositories_manager,
        charge_classifier=offense_classifier,
        image_downloader=image_downloader,
    )

    rabbitmq_consumer = RabbitMQConsumer(
        username=os.environ["RMQ_USER"],
        password=os.environ["RMQ_PASS"],
        host=os.environ["RMQ_HOST"],
        port=os.environ["RMQ_PORT"],
    )
    notice_consumer = NoticeConsumer(
        queue_name=os.environ["RMQ_NOTICE_QUEUE"],
        rmq_consumer=rabbitmq_consumer,
        consume_callback_function=notice_saver.save_notice_from_dict,
    )
    notice_consumer.run()


if __name__ == "__main__":
    main()
