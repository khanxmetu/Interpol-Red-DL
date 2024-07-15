from abc import ABC, abstractmethod, ABCMeta
from enum import Enum, EnumMeta

class CombinedMeta(EnumMeta, ABCMeta):
    pass

class CodedEnum(ABC, Enum, metaclass=CombinedMeta):
    """
    Abstract Enum class to be used for enums with data values encoded/decoded by defined codes
    By default codes are generated based on enum constant names, this property can be overridden
    """
    @property
    def code(self) -> str:
        return self.name

    @classmethod
    def get_from_code(cls, code: str) -> "CodedEnum":
        """Retrieves the enum object by code"""
        for item in cls:
            if item.code == code:
                return item
        msg = f"Input should be one of {[member.code for member in cls]}"
        msg += f" or of type {cls}"
        raise ValueError(msg)