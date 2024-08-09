import pytest
from unittest.mock import Mock, patch
from pydantic import AnyUrl
from datetime import date

from api_poller.api_request_session import APIRequestSession
from api_poller.exceptions import NoticeDetailParsingException
from api_poller.notice_detail_fetcher import NoticeImageIDsFetcher, NoticeDetailFetcher
from api_poller.models.hair_color import HairColor
from api_poller.models.eye_color import EyeColor
from api_poller.models.sex import Sex
from api_poller.models.notice import Notice
from api_poller.models.country import Country
from api_poller.models.language import Language
# Tests for NoticeImageIDsFetcher


class TestNoticeImageIDsFetcher:

    @pytest.fixture
    def session(self):
        return Mock(spec=APIRequestSession)

    @pytest.fixture
    def fetcher(self, session):
        return NoticeImageIDsFetcher(session, "http://example.com")

    def test_extract_ids_from_page_success(self, fetcher):
        data = {
            "_embedded": {
                "images": [
                    {"picture_id": "id1"},
                    {"picture_id": "id2"},
                    {"some_other_key": "value"}
                ]
            }
        }
        result = fetcher._extract_ids_from_page(data)
        assert result == ["id1", "id2"]

    def test_extract_ids_from_page_key_error(self, fetcher):
        data = {}
        with pytest.raises(NoticeDetailParsingException):
            fetcher._extract_ids_from_page(data)

    def test_fetch_image_ids_success(self, fetcher, session):
        notice_id = "notice123"
        data = {
            "_embedded": {
                "images": [
                    {"picture_id": "id1"},
                    {"picture_id": "id2"},
                    {"some_other_key": "value"}
                ]
            }
        }
        session.get_json_response.return_value = data
        result = fetcher.fetch_image_ids(notice_id)
        assert result == ["id1", "id2"]
        session.get_json_response.assert_called_once_with(
            f"http://example.com/{notice_id}/images")

# Tests for NoticeDetailFetcher


class TestNoticeDetailFetcher:

    @pytest.fixture
    def session(self):
        return Mock(spec=APIRequestSession)

    @pytest.fixture
    def image_ids_fetcher(self, session):
        return Mock(spec=NoticeImageIDsFetcher)

    @pytest.fixture
    def fetcher(self, session, image_ids_fetcher):
        return NoticeDetailFetcher(session, "http://example.com", image_ids_fetcher)

    def test_make_notice_from_embed_success(self, fetcher, image_ids_fetcher):
        data = {
            'entity_id': '123/2020',
            '_links': {'self': {'href': 'http://example.com/entity/123-2020'}},
            'name': 'Doe',
            'forename': 'John',
            'date_of_birth': '1980/01/01',
            'distinguishing_marks': 'scar',
            'weight': 70,
            'nationalities': ['US'],
            'eyes_colors_id': ['BLU'],
            'sex_id': 'M',
            'place_of_birth': 'New York',
            'arrest_warrants': None,
            'country_of_birth_id': 'US',
            'hairs_id': ['BRO'],
            'languages_spoken_ids': ['ENG'],
            'height': 1.6
        }
        image_ids_fetcher.fetch_image_ids.return_value = ['id1', 'id2']
        result = fetcher._make_notice_from_embed(data)
        assert result.notice_id == '123-2020'
        assert result.url == AnyUrl("http://example.com/entity/123-2020")
        assert result.name == 'Doe'
        assert result.forename == 'John'
        assert result.date_of_birth == date(1980, 1, 1)
        assert result.distinguishing_marks == 'scar'
        assert result.weight == 70
        assert result.nationalities == [Country.get_from_code('US')]
        assert result.eyes_colors_id == [EyeColor.get_from_code('BLU')]
        assert result.sex_id.code == 'M'
        assert result.place_of_birth == 'New York'
        assert result.arrest_warrants == None
        assert result.country_of_birth_id.code == 'US'
        assert result.hairs_id == [HairColor.get_from_code('BRO')]
        assert result.languages_spoken_ids == [Language.get_from_code('ENG')]
        assert result.height == 1.6
        assert result.image_ids == ['id1', 'id2']

    def test_fetch_notice_detail_success(self, fetcher, session, image_ids_fetcher):
        notice_id = "9304/123"
        data = {
            'entity_id': '9304/123',
            '_links': {'self': {'href': 'http://example.com/9304-123'}},
            'name': 'Doe',
            'forename': 'John',
            'date_of_birth': '1980/01/01',
            'distinguishing_marks': 'scar',
            'weight': 70,
            'nationalities': ['US'],
            'eyes_colors_id': ['BLU'],
            'sex_id': 'M',
            'place_of_birth': 'New York',
            'arrest_warrants': [],
            'country_of_birth_id': 'US',
            'hairs_id': ['BRO'],
            'languages_spoken_ids': ['ENG'],
            'height': 1.6
        }
        session.get_json_response.return_value = data
        image_ids_fetcher.fetch_image_ids.return_value = ['id1', 'id2']
        result = fetcher.fetch_notice_detail(notice_id)
        assert result.notice_id == '9304-123'
        assert result.url == AnyUrl('http://example.com/9304-123')
        assert result.name == 'Doe'
        assert result.forename == 'John'
        assert result.date_of_birth == date(1980,1,1)
        assert result.distinguishing_marks == 'scar'
        assert result.weight == 70
        assert result.nationalities == [Country.get_from_code('US')]
        assert result.eyes_colors_id == [EyeColor.get_from_code('BLU')]
        assert result.sex_id.code == 'M'
        assert result.place_of_birth == 'New York'
        assert result.arrest_warrants == []
        assert result.country_of_birth_id.code == 'US'
        assert result.hairs_id == [HairColor.get_from_code('BRO')]
        assert result.languages_spoken_ids == [Language.get_from_code('ENG')]
        assert result.height == 1.6
        assert result.image_ids == ['id1', 'id2']
        session.get_json_response.assert_called_once_with(
            f"http://example.com/{notice_id}")

    def test_fetch_notice_detail_key_error(self, fetcher, session):
        notice_id = "notice123"
        data = {}
        session.get_json_response.return_value = data
        with pytest.raises(NoticeDetailParsingException):
            fetcher.fetch_notice_detail(notice_id)
