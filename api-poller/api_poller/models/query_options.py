from pydantic import BaseModel, field_serializer, field_validator
from pydantic import ValidationInfo
from typing import Optional

from api_poller.models.sex import Sex
from api_poller.models.utils import _encode_enums_to_code
from api_poller.models.utils import _decode_enums_from_code
from api_poller.models.utils import CodedEnum
from api_poller.models.country import Country

class QueryOptions(BaseModel):
    arrestWarrantCountryId: Optional[Country] = None
    ageMin: Optional[int] = None
    ageMax: Optional[int] = None
    nationality: Optional[Country] = None
    sexId: Optional[Sex] = None
    name: Optional[str] = None
    resultPerPage: Optional[int] = 160

    @field_serializer(
        "arrestWarrantCountryId",
        "nationality",
        "sexId"
    )
    def encode_enums_to_code(obj: CodedEnum|list[CodedEnum]) -> str|list[str]:
        return _encode_enums_to_code(obj)

    @field_validator(
        "arrestWarrantCountryId",
        "nationality",
        "sexId",
        mode='before'
    )
    @classmethod
    def decode_enums_from_code(cls, obj, ctx:ValidationInfo) -> CodedEnum|list[CodedEnum]:
        field_enum_mapping: dict[str, CodedEnum] = {
            "arrestWarrantCountryId": Country,
            "nationality": Country,
            "sexId": Sex
        }
        return _decode_enums_from_code(obj, field_enum_mapping[ctx.field_name])


    def get_options_dict(self, exclude_none=True) -> dict[str, str|int]:
        return self.model_dump(exclude_none=exclude_none)