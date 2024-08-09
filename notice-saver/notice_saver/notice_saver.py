from datetime import datetime

from notice_saver.models import Notice, ImageURL, ArrestWarrant
from notice_saver.image_downloader import ImageDownloader
from notice_saver.offense_classifier import OffenseClassifier
from notice_saver.repositories_manager import RepositoriesManager
from notice_saver.exceptions import (
    ImageDownloadException,
    OffenseClassificationException,
)
from notice_saver.models import Base


class NoticeSaver:
    """
    A class to handle the saving of notice data to the database.
    """

    def __init__(
        self,
        repositories_manager: RepositoriesManager,
        image_downloader: ImageDownloader = None,
        charge_classifier: OffenseClassifier = None,
    ):
        self._repo_manager = repositories_manager
        self._image_downloader = image_downloader
        self._offense_classifier = charge_classifier

    def save_notice_from_dict(self, notice_data: dict) -> None:
        """
        Saves the notice data to database.
        If provided, it utilizes an image downloader and charge classifier
        to download notice-related images locally and assign arrest warrants' charge type respectively
        """
        notice_id = notice_data.get("notice_id")
        if self._repo_manager.notice_repository.already_exists(notice_id=notice_id):
            print(f"[+] Notice: {notice_id} already exists")
            return
        image_ids = notice_data.get("image_ids") or []
        image_urls = self.download_and_get_image_urls(
            notice_url=notice_data.get("url"), notice_id=notice_id, image_ids=image_ids
        )

        arrest_warrants = (
            self._get_arrest_warrants(
                arrest_warrants_data=notice_data.get("arrest_warrants"),
            )
            if notice_data.get("arrest_warrants")
            else []
        )

        sex = self._repo_manager.sex_repository.get_by_id(notice_data.get("sex_id"))

        country_of_birth = self._repo_manager.country_repository.get_by_id(
            notice_data.get("country_of_birth_id")
        )

        nationalities = (
            [
                self._repo_manager.country_repository.get_by_id(id)
                for id in notice_data.get("nationalities")
            ]
            if notice_data.get("nationalities")
            else []
        )

        eye_colors = (
            [
                self._repo_manager.eye_color_repository.get_by_id(id)
                for id in notice_data.get("eyes_colors_id")
            ]
            if notice_data.get("eyes_colors_id")
            else []
        )

        hair_colors = (
            [
                self._repo_manager.hair_color_repository.get_by_id(id)
                for id in notice_data.get("hairs_id")
            ]
            if notice_data.get("hairs_id")
            else []
        )

        languages_spoken = (
            [
                self._repo_manager.language_repository.get_by_id(id)
                for id in notice_data.get("languages_spoken_ids")
            ]
            if notice_data.get("languages_spoken_ids")
            else []
        )

        date_of_birth = notice_data.get("date_of_birth")
        if date_of_birth:
            date_of_birth = datetime.fromisoformat(date_of_birth)

        notice = Notice(
            id=notice_id,
            url=notice_data.get("url"),
            name=notice_data.get("name"),
            forename=notice_data.get("forename"),
            date_of_birth=date_of_birth,
            distinguishing_marks=notice_data.get("distinguishing_marks"),
            weight=notice_data.get("weight"),
            height=notice_data.get("height"),
            place_of_birth=notice_data.get("place_of_birth"),
            country_of_birth=country_of_birth,
            sex=sex,
            nationalities=nationalities,
            eye_colors=eye_colors,
            hair_colors=hair_colors,
            languages_spoken=languages_spoken,
            arrest_warrants=arrest_warrants,
            image_urls=image_urls,
        )
        try:
            self._repo_manager.notice_repository.save(notice)
            print(f"[+] Notice: {notice.id} saved successfully")
        except Exception as e:
            # TODO
            print(f"[-] Failed to save Notice: {notice.id}", e)

    def download_and_get_image_urls(
        self, notice_url: str, notice_id: str, image_ids: list[int]
    ) -> list[ImageURL]:
        """
        Constructs ImageURL objects for each image id
        and optionally downloads the image
        """
        image_url_objs = []
        for image_id in image_ids:
            original_url = f"{notice_url}/images/{image_id}"
            public_url = None
            if self._image_downloader:
                try:
                    public_url = self._image_downloader.download_and_get_public_url(
                        source_url=original_url,
                        destination_directory=notice_id,
                        file_name=image_id,
                    )
                except ImageDownloadException as e:
                    print(f"[-] Failed to download image {original_url}", e)
            image_url_obj = ImageURL(
                id=image_id, original_url=original_url, downloaded_url=public_url
            )
            image_url_objs.append(image_url_obj)
        return image_url_objs

    def _get_arrest_warrants(
        self, arrest_warrants_data: list[dict[str, str]]
    ) -> list[ArrestWarrant]:
        """
        Constructs ArrestWarrants objects for each arrest warrant
        and optionally classifies them by offense type
        """
        arrest_warrants = []
        for arrest_warrant_data in arrest_warrants_data:
            arrest_warrant = ArrestWarrant(
                charge=arrest_warrant_data.get("charge"),
                charge_translation=arrest_warrant_data.get("charge_translation"),
                issuing_country=self._repo_manager.country_repository.get_by_id(
                    arrest_warrant_data.get("issuing_country_id")
                ),
            )
            if self._offense_classifier:
                offense_explanation = arrest_warrant_data.get(
                    "charge_translation"
                ) or arrest_warrant_data.get("charge") or ""

                try:
                    arrest_warrant.offense_types = self._offense_classifier.classify(
                        offense_explanation
                    )
                except OffenseClassificationException as e:
                    print(f"Failed to classify offense: {offense_explanation}", e)
            arrest_warrants.append(arrest_warrant)
        return arrest_warrants
