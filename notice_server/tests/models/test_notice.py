from datetime import date, datetime
import pytest
from mongoengine import ValidationError, DateField

from notice_server.models.notice import Notice, ArrestWarrant


def test_arrest_warrant_none_params():
    warrant = ArrestWarrant(
        charge="Test", issuing_country_id=None, charge_translation=None)
    assert warrant.charge == "Test"
    assert warrant.issuing_country_id == None
    assert warrant.charge_translation == None


def test_arrest_warrant_default_params():
    warrant = ArrestWarrant()
    assert warrant.charge == None
    assert warrant.issuing_country_id == None
    assert warrant.charge_translation == None


def test_arrest_warrant_country_id_code_param():
    warrant = ArrestWarrant(issuing_country_id="AD")
    assert warrant.issuing_country_id == "AD"


def test_notice_no_params():
    notice = Notice()
    with pytest.raises(ValidationError):
        notice.validate()


def test_notice_only_id():
    notice = Notice(notice_id="asd")
    notice.validate()
    assert notice.notice_id == "asd"


def test_notice_default_params():
    notice = Notice(notice_id="3949", url="https://example.com")
    notice.validate()
    assert notice.name == None
    assert notice.forename == None
    assert notice.date_of_birth == None
    assert notice.distinguishing_marks == None
    assert notice.weight == None
    assert notice.nationalities in [None, []]
    assert notice.eyes_colors_id in [None, []]
    assert notice.sex_id == None
    assert notice.place_of_birth == None
    assert notice.arrest_warrants in [None, []]
    assert notice.country_of_birth_id == None
    assert notice.hairs_id in [None, []]
    assert notice.languages_spoken_ids in [None, []]
    assert notice.height == None
    assert notice.image_ids in [None, []]


def test_notice_country_of_birth_id_code_param():
    notice = Notice(notice_id="3949", url="https://example.com",
                    country_of_birth_id="AD")
    assert notice.country_of_birth_id == "AD"


def test_notice_with_arrest_warrants_param():
    warrants = [ArrestWarrant(charge="Test"), ArrestWarrant(charge="Test2")]
    notice = Notice(
        notice_id="3949",
        url="https://example.com",
        arrest_warrants=warrants
    )
    notice.validate()
    assert notice.arrest_warrants == warrants


def test_notice_date_of_birth():
    notice = Notice(notice_id="304", date_of_birth="2020-04-20")
    notice.validate()
    assert notice.date_of_birth == date(2020, 4, 20)
    notice = Notice(notice_id="304", date_of_birth=date(2020, 4, 20))
    notice.validate()
    assert notice.date_of_birth == date(2020, 4, 20)

def test_notice_first_fetched_date():
    notice = Notice(notice_id="304", date_of_birth=datetime(2000, 4, 20, 12, 54, 19))
    notice.validate()
    assert notice.date_of_birth == datetime(2000, 4, 20, 12, 54, 19)

def test_full_notice():
    data = {
        'notice_id': '123-2020',
        'name': 'Doe',
        'forename': 'John',
        'date_of_birth': '1980-01-01',
        'distinguishing_marks': 'scar',
        'weight': 70,
        'nationalities': ['US'],
        'eyes_colors_id': ['BLU'],
        'sex_id': 'M',
        'place_of_birth': 'New York',
        'arrest_warrants': [
            {
                "charge": "charge_info",
                "issuing_country_id": "UY",
                "charge_translation": None
            },
            {
                "charge": "charge_info2",
                "issuing_country_id": "US",
                "charge_translation": None
            }
        ],
        'country_of_birth_id': 'US',
        'hairs_id': ['BRO'],
        'languages_spoken_ids': ['ENG'],
        'height': 1.6,
        'image_ids': ['id1', 'id2'],
        'url': 'http://example.com/entity/123-2020',
        'last_fetched_date': datetime(2000, 4, 20, 12, 54, 19),
        'first_fetched_date': datetime(2001, 4, 20, 12, 20, 19),
        'last_modified_date': datetime(2003, 4, 19, 12, 30, 12)
    }
    notice = Notice(**data)
    notice.validate()
    assert notice.notice_id == '123-2020'
    assert notice.url == "http://example.com/entity/123-2020"
    assert notice.name == 'Doe'
    assert notice.forename == 'John'
    assert notice.date_of_birth == date(1980, 1, 1)
    assert notice.distinguishing_marks == 'scar'
    assert notice.weight == 70
    assert notice.nationalities == ["US"]
    assert notice.eyes_colors_id == ["BLU"]
    assert notice.sex_id == 'M'
    assert notice.place_of_birth == 'New York'
    assert notice.arrest_warrants == [
        ArrestWarrant(charge="charge_info", issuing_country_id="UY"),
        ArrestWarrant(charge="charge_info2", issuing_country_id="US")
    ]
    assert notice.country_of_birth_id == 'US'
    assert notice.hairs_id == ["BRO"]
    assert notice.languages_spoken_ids == ["ENG"]
    assert notice.height == 1.6
    assert notice.image_ids == ['id1', 'id2']
    assert notice.last_fetched_date == datetime(2000, 4, 20, 12, 54, 19)
    assert notice.first_fetched_date == datetime(2001, 4, 20, 12, 20, 19)
    assert notice.last_modified_date == datetime(2003, 4, 19, 12, 30, 12)
