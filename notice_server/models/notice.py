import json
from datetime import datetime

from mongoengine import Document, EmbeddedDocument, ListField
from mongoengine import StringField, IntField, FloatField
from mongoengine import EmbeddedDocumentListField, DateTimeField, URLField, DateField


COUNTRIES = json.load(open('models/country_codes.json')).keys()
LANGUAGES = json.load(open('models/language_codes.json')).keys()
EYES = json.load(open('models/eye_color_codes.json')).keys()
HAIRS = json.load(open('models/hair_color_codes.json')).keys()
SEXES = json.load(open('models/sex_codes.json')).keys()



class ArrestWarrant(EmbeddedDocument):
    charge = StringField(max_length=2000)
    issuing_country_id = StringField(choices=COUNTRIES)
    charge_translation = StringField(max_length=2000)


class Notice(Document):
    notice_id = StringField(primary_key=True, max_length=20, required=True)
    date_of_birth = DateField(max_length=20)
    distinguishing_marks = StringField(max_length=250)
    weight = IntField(min_value=0, max_value=150)
    nationalities = ListField(StringField(choices=COUNTRIES))
    eyes_colors_id = ListField(StringField(choices=EYES))
    sex_id = StringField(choices=SEXES, default='U')
    place_of_birth = StringField(max_length=100)
    forename = StringField(max_length=100)
    arrest_warrants = EmbeddedDocumentListField(ArrestWarrant)
    country_of_birth_id = StringField(choices=COUNTRIES)
    hairs_id = ListField(StringField(choices=HAIRS))
    name = StringField(max_length=100, required=True)
    languages_spoken_ids = ListField(StringField(choices=LANGUAGES))
    height = FloatField(min_value=0, max_value=2)
    image_ids = ListField(StringField(max_length=20))
    last_fetched_date = DateTimeField(default=datetime.now)
    last_modified_date = DateTimeField(default=datetime.now)
    first_fetched_date = DateTimeField(default=datetime.now)
    url = URLField()

    def __eq__(self, other):
        if self is other: return True
        elif type(self) != type(other): return False
        field_names = self._fields
        for field in field_names:
            if field in ['last_fetched_date', 'last_modified_date', 'first_fetched_date']:
                continue
            if self[field] != other[field]:
                return False
        return True