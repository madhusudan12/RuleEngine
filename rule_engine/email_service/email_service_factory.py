
from rule_engine.email_service.email_service import GmailService
from rule_engine.email_service.services import ServiceType


class EmailServiceFactory:
    @staticmethod
    def create_service(service_type, credentials_file):
        if service_type == ServiceType.GMAIL.value:
            return GmailService(credentials_file)
        else:
            raise ValueError('Unsupported service type')
