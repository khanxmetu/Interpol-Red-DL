from pydantic import ValidationError
import pytest

from api_poller.models.query_options import QueryOptions
from api_poller.models.country import Country

def test_query_options_fields_valid():
    options = QueryOptions(nationality="AD", ageMin=20, ageMax=30)
    assert options.nationality == Country.get_from_code("AD")
    assert options.ageMin == 20
    assert options.ageMax == 30


def test_query_options_fields_invalid():
    with pytest.raises(ValidationError):
        options = QueryOptions(nationality="ASDASD", ageMin=20, ageMax=30)

def test_query_options_field_default():
    options = QueryOptions()
    assert options.nationality == None
    assert options.ageMin == None
    assert options.ageMax == None

def test_query_options_get_options_dict_default():
    options = QueryOptions()
    assert options.get_options_dict() == {}

def test_query_options_get_options_dict():
    options = QueryOptions(nationality=Country._914)
    assert options.get_options_dict() == {"nationality": "914"}

