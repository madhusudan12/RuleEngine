from rule_engine.email_service.email_service import GmailService, EmailService
from rule_engine.email_service.services import ServiceType


class EmailServiceFactory:
    @staticmethod
    def create_service(service_type: str, credentials_file: str) -> EmailService:
        if service_type == ServiceType.GMAIL.value:
            return GmailService(credentials_file)
        else:
            raise ValueError('Unsupported service type')
