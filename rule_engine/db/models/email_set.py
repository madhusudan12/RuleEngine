from rule_engine.db.models.email import Email
from rule_engine.rules.rule_set import RuleSet


class EmailSet:
    def __init__(self):
        self.emails = set()

    def add_email(self, email:Email):
        self.emails.add(email)

    def get_list(self):
        return self.emails

    def filter(self, rule_set:RuleSet):
        filtered_set = set()
        for email in self.emails:

            pass