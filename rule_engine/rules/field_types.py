
from enum import Enum

class FieldTypes(Enum):
    DATE_FIELD = "received_date"
    TO_FIELD = "to_email"
    FROM_FIELD = "from_email"
    SUBJECT_FIELD = "subject"
    MESSAGE_FIELD = "message"
