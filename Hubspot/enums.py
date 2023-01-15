import enum


class BaseHSObjects(str, enum.Enum):
    CONTACT = "0-1"
    COMPANY = "0-2"
    DEAL = "0-3"
    TICKET = "0-5"
