import json

from rule_engine.rules.rule_factory import RuleFactory
from rule_engine.rules.rule_set import RuleSet
from rule_engine.actions.action_factory import ActionFactory


class RuleProcessor:
    def __init__(self, rules_file, email_service):
        self.email_service = email_service
        self.action_factory = ActionFactory(email_service)
        self.rule_sets = self.load_rules(rules_file)

    def load_rules(self, rules_file):
        with open(rules_file, 'r') as file:
            data = json.load(file)
        rule_sets = []
        for rule_set_data in data['rule_sets']:
            rules = [
                RuleFactory.create_rule(rule['field'], rule['predicate'], rule['value'])
                for rule in rule_set_data['rules']
            ]
            actions = [
                self.action_factory.create_action(action)
                for action in rule_set_data['actions']
            ]
            rule_sets.append(RuleSet(rules, rule_set_data['predicate'], actions))
        return rule_sets

    def process_emails(self, emails):
        for email in emails:
            for rule_set in self.rule_sets:
                if rule_set.matches(email):
                    for action in rule_set.actions:
                        action.execute(email)
