import pytest
from pydantic import ValidationError

from api_poller.models.notice import Notice, ArrestWarrant
from api_poller.models.country import Country
from api_poller.models.language import Language
from api_poller.models.hair_color import HairColor
from api_poller.models.sex import Sex

def test_arrest_warrant_none_params():
    warrant = ArrestWarrant(charge="Test", issuing_country_id=None, charge_translation=None)

def test_arrest_warrant_default_params():
    warrant = ArrestWarrant()
    assert warrant.charge == None
    assert warrant.issuing_country_id == None
    assert warrant.charge_translation == None

def test_arrest_warrant_country_id_code_param():
    warrant = ArrestWarrant(issuing_country_id="AD")
    assert warrant.issuing_country_id == Country.get_from_code("AD")

def test_arrest_warrant_country_id_enum_param():
    warrant = ArrestWarrant(issuing_country_id=Country.AD)
    assert warrant.issuing_country_id == Country.AD

def test_arrest_warrant_country_id_enum_value_param():
    with pytest.raises(ValidationError):
        warrant = ArrestWarrant(issuing_country_id="Andorra")


def test_notice_no_params():
    with pytest.raises(ValidationError):
        notice = Notice()

def test_notice_default_params():
    notice = Notice(notice_id="3949", url="https://example.com")
    assert notice.name == None
    assert notice.forename == None
    assert notice.date_of_birth == None
    assert notice.distinguishing_marks == None
    assert notice.weight == None
    assert notice.nationalities == None
    assert notice.eyes_colors_id == None
    assert notice.sex_id == None
    assert notice.place_of_birth == None
    assert notice.arrest_warrants == None
    assert notice.country_of_birth_id == None
    assert notice.hairs_id == None
    assert notice.languages_spoken_ids == None
    assert notice.height == None
    assert notice.image_ids == None

def test_notice_country_of_birth_id_code_param():
    notice = Notice(notice_id="3949", url="https://example.com", country_of_birth_id="AD")
    assert notice.country_of_birth_id == Country.get_from_code("AD")

def test_notice_country_of_birth_id_enum_param():
    notice = Notice(notice_id="3949", url="https://example.com", country_of_birth_id=Country.AD)
    assert notice.country_of_birth_id == Country.AD

def test_notice_country_of_birth_id_enum_value_param():
    with pytest.raises(ValidationError):
        notice = Notice(notice_id="3949", url="https://example.com", country_of_birth_id="Andorra")


def test_notice_languages_spoken_ids_code_param():
    notice = Notice(notice_id="3949", url="https://example.com", languages_spoken_ids=["AFR", "ALB"])
    assert notice.languages_spoken_ids == [Language.get_from_code("AFR"), Language.get_from_code("ALB")]

def test_notice_languages_spoken_ids_enum_param():
    notice = Notice(notice_id="3949", url="https://example.com", languages_spoken_ids=[Language.AFR, Language.ALB])
    assert notice.languages_spoken_ids == [Language.AFR, Language.ALB]

def test_notice_languages_spoken_ids_enum_value_param():
    with pytest.raises(ValidationError):
        notice = Notice(notice_id="3949", url="https://example.com", languages_spoken_ids=["Afrikaans", "Albanian"])


def test_notice_hairs_id_code_param():
    notice = Notice(notice_id="3949", url="https://example.com", hairs_id=["BLA", "BRO"])
    assert notice.hairs_id == [HairColor.get_from_code("BLA"), HairColor.get_from_code("BRO")]

def test_notice_hairs_id_enum_param():
    notice = Notice(notice_id="3949", url="https://example.com", hairs_id=[HairColor.BLA, HairColor.BRO])
    assert notice.hairs_id == [HairColor.BLA, HairColor.BRO]

def test_notice_hairs_id_enum_value_param():
    with pytest.raises(ValidationError):
        notice = Notice(notice_id="3949", url="https://example.com", hairs_id=["Black", "Brown"])

def test_notice_with_arrest_warrants_param():
    warrants = [ArrestWarrant(charge="Test"), ArrestWarrant(charge="Test2")]
    notice = Notice(
        notice_id="3949",
        url="https://example.com",
        arrest_warrants=warrants
        )
    assert notice.arrest_warrants == warrants

def test_warrant_to_json():
    warrant = ArrestWarrant(charge="Test", issuing_country_id=Country.get_from_code("AD"), charge_translation="asd")
    expected_json = '{"charge":"Test","issuing_country_id":"AD","charge_translation":"asd"}'
    assert warrant.model_dump_json() == expected_json

def test_notice_to_json():
    warrants = [ArrestWarrant(charge="Test", issuing_country_id=Country.AD), ArrestWarrant(charge="Test2")]
    notice = Notice(
        notice_id="3949",
        url="https://example.com",
        arrest_warrants=warrants,
        sex_id=Sex.M
        )
    expected_json = '{"notice_id":"3949","url":"https://example.com/","name":null,"forename":null,"date_of_birth":null,"distinguishing_marks":null,"weight":null,"nationalities":null,"eyes_colors_id":null,"sex_id":"M","place_of_birth":null,"arrest_warrants":[{"charge":"Test","issuing_country_id":"AD","charge_translation":null},{"charge":"Test2","issuing_country_id":null,"charge_translation":null}],"country_of_birth_id":null,"hairs_id":null,"languages_spoken_ids":null,"height":null,"image_ids":null}'
    assert notice.model_dump_json() == expected_json

def test_notice_to_json_with_list_of_coded_enums():
    notice = Notice(
        notice_id="2323",
        url="https://example.com",
        languages_spoken_ids=[Language.AFA, Language.ALB]
    )
    expected_json = '{"notice_id":"2323","url":"https://example.com/","name":null,"forename":null,"date_of_birth":null,"distinguishing_marks":null,"weight":null,"nationalities":null,"eyes_colors_id":null,"sex_id":null,"place_of_birth":null,"arrest_warrants":null,"country_of_birth_id":null,"hairs_id":null,"languages_spoken_ids":["AFA","ALB"],"height":null,"image_ids":null}'
    assert notice.model_dump_json() == expected_json

def test_notice_to_json_with_code_enum():
    notice = Notice(notice_id="2323", url="https://example.com", country_of_birth_id=Country._914)
    assert notice.model_dump_json(exclude_none=True) == '{"notice_id":"2323","url":"https://example.com/","country_of_birth_id":"914"}'