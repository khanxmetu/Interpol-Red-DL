from api_poller.models.coded_enum import CodedEnum


class HairColor(CodedEnum):
    BLA = "Black"
    BRO = "Brown"
    BROF = "Fair"
    GRY = "Grey"
    GRYG = "Greying"
    HAIB = "Bald"
    HAID = "Dyed"
    OTHD = "Dark"
    RED = "Red"
    REDA = "Auburn"
    WHI = "White"
    YELB = "Blond"

    @classmethod
    def get_from_code(cls, code: str) -> CodedEnum:
        # Make it compatable with legacy hair codes
        if code == "YELBD" or code == "BROL":
            return HairColor.YELB
        return super().get_from_code(code)