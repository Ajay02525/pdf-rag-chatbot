from enum import Enum


class Intent(str, Enum):
    DOCUMENT_QA = "DOCUMENT_QA"

    GENERAL = "GENERAL"

    UNKNOWN = "UNKNOWN"
