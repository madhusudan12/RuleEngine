class Email:
    def __init__(self, id, from_email, to_email, subject, message, received_date):
        self.id = id
        self.from_email = from_email
        self.to_email = to_email
        self.subject = subject
        self.message = message
        self.received_date = received_date
