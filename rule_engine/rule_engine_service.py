from rule_engine.db.models.email import Email


class RuleEngine:
    def __init__(self, email_repository):
        self.email_repository = email_repository

    def fetch_and_write_emails(self, email_service, max_results=100):
        emails_data = email_service.fetch_emails(max_results=max_results)
        email_objects = [
            Email(email_data['id'], email_data['from'], email_data['to'], email_data['subject'], email_data['message'],
                  email_data['received_date'])
            for email_data in emails_data
        ]
        self.email_repository.bulk_insert_emails(email_objects)

    def process_emails(self, rule_processor):
        stored_emails = self.email_repository.fetch_emails()
        rule_processor.process_emails(stored_emails)
