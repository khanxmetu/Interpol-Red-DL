from pydantic import BaseModel, field_serializer, field_validator
from pydantic import ValidationInfo, AnyHttpUrl
from typing import Optional
from datetime import date

from api_poller.models.coded_enum import CodedEnum
from api_poller.models.eye_color import EyeColor
from api_poller.models.hair_color import HairColor
from api_poller.models.language import Language
from api_poller.models.country import Country
from api_poller.models.sex import Sex

def _encode_enums_to_code(obj: CodedEnum|list[CodedEnum]):
    if isinstance(obj, CodedEnum):
        return obj.name
    elif type(obj) == list:
        return [x.code if isinstance(x, CodedEnum) else x for x in obj]

def _decode_enums_from_code(
        obj: list[str]|str|list[CodedEnum]|CodedEnum,
        related_enum: CodedEnum
    ) -> CodedEnum:
    if isinstance(obj, list):
        return [
            related_enum.get_from_code(item) 
                if isinstance(item, str) else item for item in obj
        ]
    elif isinstance(obj, str):
        return related_enum.get_from_code(obj)
    else:
        return obj

        
class ArrestWarrant(BaseModel):
    charge: Optional[str] = None
    issuing_country_id: Optional[Country] = None
    charge_translation: Optional[str] = None

    @field_serializer(
        "issuing_country_id",
    )
    def encode_enums_to_code(obj: CodedEnum|list[CodedEnum]):
        return _encode_enums_to_code(obj)

    @field_validator(
        "issuing_country_id",
        mode='before'
    )
    @classmethod
    def decode_enums_from_code(cls, obj, ctx:ValidationInfo) -> Country:
        field_enum_mapping: dict[str, CodedEnum] = {
            "issuing_country_id": Country
        }
        return _decode_enums_from_code(obj, field_enum_mapping[ctx.field_name])


class Notice(BaseModel):
    notice_id: str
    url: AnyHttpUrl
    name: Optional[str] = None
    forename: Optional[str] = None
    date_of_birth: Optional[date] = None
    distinguishing_marks: Optional[str] = None
    weight: Optional[int] = None
    nationalities: Optional[list[Country]] = None
    eyes_colors_id: Optional[list[EyeColor]] = None
    sex_id: Sex = None
    place_of_birth: Optional[str] = None
    arrest_warrants: Optional[list[ArrestWarrant]] = None
    country_of_birth_id: Optional[Country] = None
    hairs_id: Optional[list[HairColor]] = None
    languages_spoken_ids: Optional[list[Language]] = None
    height: Optional[list[int]] = None
    image_ids: Optional[list[str]] = None

    @field_serializer(
        "nationalities",
        "eyes_colors_id",
        "sex_id",
        "country_of_birth_id",
        "hairs_id",
        "languages_spoken_ids",
    )
    def encode_enums_to_code(obj: CodedEnum|list[CodedEnum]):
        return _encode_enums_to_code(obj)

    @field_validator(
        "nationalities",
        "eyes_colors_id",
        "sex_id",
        "country_of_birth_id",
        "hairs_id",
        "languages_spoken_ids",
        mode='before'
    )
    @classmethod
    def decode_enums_from_code(cls, obj, ctx:ValidationInfo) -> Country:
        field_enum_mapping: dict[str, CodedEnum] = {
            "nationalities": Country,
            "eyes_colors_id": EyeColor,
            "sex_id": Sex,
            "country_of_birth_id": Country,
            "hairs_id": HairColor,
            "languages_spoken_ids": Language
        }
        return _decode_enums_from_code(obj, field_enum_mapping[ctx.field_name])
