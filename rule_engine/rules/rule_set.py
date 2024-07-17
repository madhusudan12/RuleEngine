
from rule_engine.rules.predicate_types import PredicateTypes


class RuleSet:
    def __init__(self, rules, predicate, actions):
        self.rules = rules
        self.predicate = predicate
        self.actions = actions

    def matches(self, email):
        results = [rule.matches(email) for rule in self.rules]
        if self.predicate == PredicateTypes.ANY.value:
            return any(results)
        elif self.predicate == PredicateTypes.ALL.value:
            return all(results)
        return False
