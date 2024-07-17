from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def execute(self, email):
        pass


class EmailAction(Action):
    def __init__(self, email_service):
        self.email_service = email_service

    def execute(self, email):
        pass


class MarkAsReadAction(EmailAction):
    def __init__(self, email_service):
        super().__init__(email_service)

    def execute(self, email):
        self.email_service.mark_as_read(email)


class MarkAsUnreadAction(EmailAction):
    def __init__(self, email_service):
        super().__init__(email_service)

    def execute(self, email):
        self.email_service.mark_as_un_read(email)


class MoveMessageAction(EmailAction):
    def __init__(self, email_service, label_id):
        super().__init__(email_service)
        self.label_id = label_id


    def execute(self, email):
        self.email_service.move_message(email, self.label_id)
