from api_poller.models.coded_enum import CodedEnum


def _encode_enums_to_code(obj: CodedEnum|list[CodedEnum]) -> str|list[str]:
    """Returns corresponding code(s) for the CodedEnum object(s)"""
    if isinstance(obj, CodedEnum):
        return obj.name
    elif type(obj) == list:
        return [x.code if isinstance(x, CodedEnum) else x for x in obj]

def _decode_enums_from_code(
        obj: list[str]|str|list[CodedEnum]|CodedEnum,
        related_enum: CodedEnum
    ) -> CodedEnum|list[CodedEnum]:
    """Returns corresponding CodedEnum object(s) from code(s) or CodedEnum object(s)"""
    if isinstance(obj, list):
        return [
            related_enum.get_from_code(item) 
                if isinstance(item, str) else item for item in obj
        ]
    elif isinstance(obj, str):
        return related_enum.get_from_code(obj)
    else:
        return obj