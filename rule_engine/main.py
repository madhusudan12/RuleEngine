
import json

from rule_engine.rule_engine_service import RuleEngine
from rule_engine.email_service.email_service_factory import EmailServiceFactory
from rule_engine.db.repository.email_repository import EmailRepository
from rule_engine.rules.rule_processor import RuleProcessor


def fetch_and_write_emails():
    # Connect to email service and database
    gmail_service = EmailServiceFactory.create_service("gmail", credential_file_path)
    email_repo = EmailRepository(db_config)

    # read emails from the mail server and write to DB
    rule_engine_service = RuleEngine(email_repo)
    rule_engine_service.fetch_and_write_emails(gmail_service, max_results=100)


def process_rules_on_emails():
    # Connect to email service and database
    gmail_service = EmailServiceFactory.create_service("gmail", credential_file_path)
    email_repo = EmailRepository(db_config)
    rule_engine_service = RuleEngine(email_repo)

    # process the emails based on the rules
    rule_processor = RuleProcessor(rules_file_path, gmail_service)
    rule_engine_service.process_emails(rule_processor)


if __name__ == '__main__':
    db_config_file_path = "data/db_config.json"
    with open(db_config_file_path, 'r') as db_file:
        db_config = json.load(db_file)
    credential_file_path = '/Users/madhusudan/Downloads/google_auth.json'
    rules_file_path = 'data/test_rules.json'

    # call this only when you need to fetch the emails and write to db
    fetch_and_write_emails()

    # call this to process all the emails in the DB
    process_rules_on_emails()
