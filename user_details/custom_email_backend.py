from django.core.mail.backends.smtp import EmailBackend

class CustomEmailBackend(EmailBackend):
    def send_messages(self, email_messages):
        for message in email_messages:
            super().send_messages([message])
