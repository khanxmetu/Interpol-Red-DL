import json
from datetime import date, datetime

from mongoengine import Document, EmbeddedDocument, ListField
from mongoengine import StringField, IntField, FloatField
from mongoengine import EmbeddedDocumentListField, DateTimeField, URLField, DateField


COUNTRIES = json.load(open('notice_server/models/country_codes.json')).keys()
LANGUAGES = json.load(open('notice_server/models/language_codes.json')).keys()
EYES = json.load(open('notice_server/models/eye_color_codes.json')).keys()
HAIRS = json.load(open('notice_server/models/hair_color_codes.json')).keys()
SEXES = json.load(open('notice_server/models/sex_codes.json')).keys()



class ArrestWarrant(EmbeddedDocument):
    charge = StringField(max_length=2000)
    issuing_country_id = StringField(choices=COUNTRIES)
    charge_translation = StringField(max_length=2000)


class Notice(Document):
    notice_id = StringField(primary_key=True, max_length=20, required=True)
    name = StringField(max_length=100)
    date_of_birth = DateField(max_length=20)
    distinguishing_marks = StringField(max_length=250)
    weight = IntField(min_value=0, max_value=150)
    nationalities = ListField(StringField(choices=COUNTRIES))
    eyes_colors_id = ListField(StringField(choices=EYES))
    sex_id = StringField(choices=SEXES)
    place_of_birth = StringField(max_length=100)
    forename = StringField(max_length=100)
    arrest_warrants = EmbeddedDocumentListField(ArrestWarrant)
    country_of_birth_id = StringField(choices=COUNTRIES)
    hairs_id = ListField(StringField(choices=HAIRS))
    languages_spoken_ids = ListField(StringField(choices=LANGUAGES))
    height = FloatField(min_value=0, max_value=2)
    url = URLField()
    image_ids = ListField(StringField(max_length=20))
    last_fetched_date = DateTimeField(default=datetime.now)
    last_modified_date = DateTimeField(default=datetime.now)
    first_fetched_date = DateTimeField(default=datetime.now)

    def clean(self):
        # Convert date_of_birth string to datetime.date object
        if isinstance(self.date_of_birth, str):
            self.date_of_birth = date.fromisoformat(self.date_of_birth)
        super().clean()


    def __eq__(self, other):
        """
        Equality of two notice objects is determined based on fields
        excluding metadata. Following fields are excluded:
        last_fetched_date, last_modified_date, first_fetched_date
        """
        if self is other: return True
        elif type(self) != type(other): return False
        field_names = self._fields
        for field in field_names:
            if field in ['last_fetched_date', 'last_modified_date', 'first_fetched_date']:
                continue
            if self[field] != other[field]:
                return False
        return True