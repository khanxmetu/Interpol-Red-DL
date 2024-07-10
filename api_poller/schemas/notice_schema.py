from marshmallow import Schema, fields, validate
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

class EmbeddedSchema(Schema):
    links = fields.List(fields.String())

class LinkSchema(Schema):
    href = fields.String()

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
    weight = fields.String(allow_none=True)
    nationalities = list_field_consists_consts(COUNTRIES, True)
    entity_id = fields.String(allow_none=True, required=True)
    eyes_colors_id = list_field_consists_consts(EYES, True)
    sex_id = field_consists_consts(SEXES, True)
    place_of_birth = fields.String(allow_none=True)
    forename = fields.String(allow_none=True)
    arrest_warrants = fields.Nested(ArrestWarrantSchema, many=True)
    country_of_birth_id = field_consists_consts(COUNTRIES, True)
    hairs_id = list_field_consists_consts(HAIRS, True)
    name = fields.String(allow_none=True)
    languages_spoken_ids = list_field_consists_consts(LANGUAGES, True)
    height = fields.String(allow_none=True)
    _embedded = fields.Nested(EmbeddedSchema)
    _links = fields.Nested(LinksSchema)

notice_schema = NoticeSchema()

def validate_notice_data(data: dict, notice_schema: Schema = notice_schema):
    return notice_schema.validate(data)