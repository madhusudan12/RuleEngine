
from datetime import datetime, timedelta


class Rule:
    def __init__(self, field, predicate, value):
        self.field = field
        self.predicate = predicate
        self.value = value

    def matches(self, email):
        raise NotImplementedError


class StringFieldRule(Rule):
    def matches(self, email):
        email_value = getattr(email, self.field, '')
        if email_value is None:
            email_value = ""
        if self.predicate == 'contains':
            return self.value in email_value
        elif self.predicate == 'does not contain':
            return self.value not in email_value
        elif self.predicate == 'equals':
            return self.value == email_value
        elif self.predicate == 'does not equal':
            return self.value != email_value
        return False


class DateFieldRule(Rule):
    def matches(self, email):
        email_value = getattr(email, self.field)
        if isinstance(email_value, datetime):
            email_value = email_value.strftime('%Y-%m-%d')
        email_value = datetime.strptime(email_value, '%Y-%m-%d')
        value = datetime.now() - timedelta(days=int(self.value))
        if self.predicate == 'less than':
            return email_value < value
        elif self.predicate == 'greater than':
            return email_value > value
        return False
