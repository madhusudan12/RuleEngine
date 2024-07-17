
from enum import Enum

class PredicateTypes(Enum):
    ALL = "All"
    ANY = "Any"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    LESS_THAN = "less_than"
    GREATER_THAN = "greater_than"

