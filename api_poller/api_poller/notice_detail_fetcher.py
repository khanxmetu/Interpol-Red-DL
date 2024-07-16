from api_poller.api_request_session import APIRequestSession
from api_poller.models.notice import Notice
from api_poller.exceptions import NoticeDetailParsingException


class NoticeImageIDsFetcher:
    def __init__(self, session: APIRequestSession, base_url: str):
        self._session = session
        self._base_url = base_url

    def _extract_ids_from_page(self, data: dict) -> list[str]:
        try:
            images_details: list[dict] = data["_embedded"]["images"]
            image_ids = [
                item["picture_id"]
                for item in images_details if item.get("picture_id")
            ]
        except KeyError as e:
            raise NoticeDetailParsingException(e)
        return image_ids

    def fetch_image_ids(self, notice_id: str) -> list[str]:
        url = f"{self._base_url}/{notice_id}/images"
        resp_dict = self._session.get_json_response(url)
        return self._extract_ids_from_page(resp_dict)


class NoticeDetailFetcher:
    def __init__(self,
                 session: APIRequestSession,
                 base_url: str,
                 notce_image_ids_fetcher: NoticeImageIDsFetcher
                 ):
        self._session = session
        self._base_url = base_url
        self._image_ids_fetcher = notce_image_ids_fetcher

    def _make_notice_from_embed(self, data: dict) -> Notice:
        notice_id = data['entity_id'].replace('/', '-')
        notice = Notice(
            notice_id=notice_id,
            url=data['_links']['self']['href'],
            name=data['name'],
            forename=data['forename'],
            date_of_birth=data['date_of_birth'].replace('/', '-'),
            distinguishing_marks=data['distinguishing_marks'],
            weight=data['weight'],
            nationalities=data['nationalities'],
            eyes_colors_id=data['eyes_colors_id'],
            sex_id=data['sex_id'],
            place_of_birth=data['place_of_birth'],
            arrest_warrants=data['arrest_warrants'],
            country_of_birth_id=data['country_of_birth_id'],
            hairs_id=data['hairs_id'],
            languages_spoken_ids=data['languages_spoken_ids'],
            height=data['height'],
            image_ids=self._image_ids_fetcher.fetch_image_ids(notice_id)
        )
        return notice

    def fetch_notice_detail(self, notice_id: str) -> Notice:
        """Returns a Notice object containing necessary details fetched from api"""
        url = f"{self._base_url}/{notice_id}"
        data = self._session.get_json_response(url)
        try:
            return self._make_notice_from_embed(data)
        except KeyError as e:
            raise NoticeDetailParsingException(e)
