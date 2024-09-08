from abc import ABC, abstractmethod

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


class EmailSender(ABC):
    @abstractmethod
    def send_email(self, recipient_list: list, fail_silently=False):
        pass


class SuccessEmailSender(EmailSender):
    def __init__(self, event: object):
        self.creator = event

    def send_email(self, recipient_list: list, fail_silently=False):
        send_mail(
            "Вітаю!",
            "Ваш івент одобрено!",
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=fail_silently,
        )


class RejectEmailSender(EmailSender):
    def __init__(self, event: object):
        self.event = event

    def send_email(self, recipient_list: list, fail_silently=False):
        send_mail(
            "Відмова",
            f"Відмова по причині: {self.event.feedback}",
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=fail_silently,
        )


class EmailController:
    def __init__(self, event: object):
        self.event = event

    def get_sender(self):
        if self.event.result_revue == "approved":
            return SuccessEmailSender(self.event)
        else:
            return RejectEmailSender(self.event)

    def send_email(self, recipient_list: list, fail_silently=False):
        sender = self.get_sender()
        sender.send_email(recipient_list, fail_silently)
