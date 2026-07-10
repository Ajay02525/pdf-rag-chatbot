import re


class OutputPIIGuardrail:
    @staticmethod
    def sanitize(text: str):

        text = re.sub(
            r"\b(?:\+91[- ]?)?[6-9]\d{9}\b",
            "**********",
            text,
        )

        text = re.sub(
            r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
            "**********",
            text,
        )

        text = re.sub(
            r"\b\d{4}\s?\d{4}\s?\d{4}\b",
            "************",
            text,
        )

        return text
