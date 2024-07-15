from marshmallow import Schema, fields, validate, ValidationError, pre_load
import json

COUNTRIES = json.load(open('schemas/country_codes.json')).keys()
LANGUAGES = json.load(open('schemas/language_codes.json')).keys()
EYES = json.load(open('schemas/eye_color_codes.json')).keys()
HAIRS = json.load(open('schemas/hair_color_codes.json')).keys()
SEXES = json.load(open('schemas/sex_codes.json')).keys()

def field_consists_consts(
        constants: tuple, allow_none=False
) -> fields.String:
    return fields.String(validate=validate.OneOf(constants), allow_none=allow_none)

def list_field_consists_consts(
        constants: tuple, allow_none=False
) -> fields.List:
    return fields.List(field_consists_consts(constants, allow_none), allow_none=allow_none)

def field_int_or_null() -> fields.Field:
    def validate_int_or_null(value):
        if value is not None and not isinstance(value, int):
            raise ValidationError("Field should be null or an integer.")
    return fields.Field(allow_none=True, validate=validate_int_or_null)

def field_float_or_null() -> fields.Field:
    def validate_float_or_null(value):
        not_float = not isinstance(value, float)
        not_int = not isinstance(value, int)
        if value is not None and not_float and not_int:
            raise ValidationError("Field should be null or an float.")
    return fields.Field(allow_none=True, validate=validate_float_or_null)

class EmbeddedSchema(Schema):
    links = fields.List(fields.String())

class LinkSchema(Schema):
    href = fields.URL()

class LinksSchema(Schema):
    self = fields.Nested(LinkSchema)
    images = fields.Nested(LinkSchema)
    thumbnail = fields.Nested(LinkSchema)

class ArrestWarrantSchema(Schema):
    charge = fields.String()
    issuing_country_id = field_consists_consts(COUNTRIES, True)
    charge_translation = fields.String(allow_none=True)

class NoticeSchema(Schema):
    date_of_birth = fields.String(allow_none=True)
    distinguishing_marks = fields.String(allow_none=True)
    weight = field_int_or_null()
    nationalities = list_field_consists_consts(COUNTRIES, True)
    entity_id = fields.String(required=True)
    eyes_colors_id = list_field_consists_consts(EYES, True)
    sex_id = field_consists_consts(SEXES, True)
    place_of_birth = fields.String(allow_none=True)
    forename = fields.String(allow_none=True)
    arrest_warrants = fields.Nested(ArrestWarrantSchema, many=True)
    country_of_birth_id = field_consists_consts(COUNTRIES, True)
    hairs_id = list_field_consists_consts(HAIRS, True)
    name = fields.String(allow_none=True)
    languages_spoken_ids = list_field_consists_consts(LANGUAGES, True)
    height = field_float_or_null()
    _embedded = fields.Nested(EmbeddedSchema)
    _links = fields.Nested(LinksSchema)

class NewNoticeSchema(NoticeSchema):
    notice_id = fields.String(required=True)
    img_ids = fields.List(fields.String())

    class Meta:
        exclude = ('_embedded', '_links', 'entity_id')


notice_schema = NoticeSchema()
new_notice_schema = NewNoticeSchema()

def validate_notice_data(data: dict, notice_schema: Schema = notice_schema) -> dict:
    return notice_schema.validate(data)