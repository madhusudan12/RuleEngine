
from rule_engine.rules.rules import StringFieldRule, DateFieldRule
from rule_engine.rules.field_types import FieldTypes


class RuleFactory:
    @staticmethod
    def create_rule(field, predicate, value):
        if field in (FieldTypes.FROM_FIELD.value, FieldTypes.TO_FIELD.value,
                     FieldTypes.MESSAGE_FIELD.value, FieldTypes.SUBJECT_FIELD.value):
            return StringFieldRule(field, predicate, value)
        elif field == FieldTypes.DATE_FIELD.value:
            return DateFieldRule(field, predicate, value)
        else:
            raise ValueError(f"Unsupported field: {field}")

