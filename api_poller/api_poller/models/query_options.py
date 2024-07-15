from pydantic import BaseModel, field_serializer, field_validator
from pydantic import ValidationInfo
from typing import Optional

from api_poller.models.utils import _encode_enums_to_code
from api_poller.models.utils import _decode_enums_from_code
from api_poller.models.utils import CodedEnum
from api_poller.models.country import Country

class QueryOptions(BaseModel):
    nationality: Optional[Country] = None
    ageMin: Optional[int] = None
    ageMax: Optional[int] = None
    arrestWarrantCountryId: Optional[Country] = None
    resultPerPage: Optional[int] = 160

    @field_serializer(
        "arrestWarrantCountryId",
        "nationality"
    )
    def encode_enums_to_code(obj: CodedEnum|list[CodedEnum]) -> str|list[str]:
        return _encode_enums_to_code(obj)

    @field_validator(
        "arrestWarrantCountryId",
        "nationality",
        mode='before'
    )
    @classmethod
    def decode_enums_from_code(cls, obj, ctx:ValidationInfo) -> CodedEnum|list[CodedEnum]:
        field_enum_mapping: dict[str, CodedEnum] = {
            "arrestWarrantCountryId": Country,
            "nationality": Country
        }
        return _decode_enums_from_code(obj, field_enum_mapping[ctx.field_name])


    def get_options_dict(self, exclude_none=True) -> dict[str, str|int]:
        return self.model_dump(exclude_none=exclude_none)