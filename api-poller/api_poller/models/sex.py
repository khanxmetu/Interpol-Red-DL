from api_poller.models.coded_enum import CodedEnum


class Sex(CodedEnum):
    M = "Male"
    F = "Female"
    U = "Unknown"