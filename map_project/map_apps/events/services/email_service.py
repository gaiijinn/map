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


class BaseSubscriberEmailGetter:
    def get_subscriber_emails(self, creator_obj):
        pass


class SubscriberEmailGetter(BaseSubscriberEmailGetter):
    def __init__(self, creator_obj):
        self.creator_obj = creator_obj

    def get_subscriber_emails(self):
        subscribers = self.creator_obj.subscriptions_received.all()
        emails = [subscriber.email for subscriber in subscribers]
        return emails


class EventLinkGenerator:
    def __init__(self, event_obj):
        self.event = event_obj

    def generate_link(self):
        domain = settings.DOMAIN_NAME
        port = settings.PORT
        event_url = reverse("events:events-detail", kwargs={'pk': self.event.id})

        return f"{domain}:{port}{event_url}"


class EmailToSubscribers(EmailSender):
    def __init__(self, event_obj, email_getter=SubscriberEmailGetter, link_generator=EventLinkGenerator):
        self.event = event_obj
        self.creator = event_obj.creator

        self.email_obj = email_getter(self.creator)
        self.link_obj = link_generator(self.event)

    def send_email(self, recipient_list: list, fail_silently=False):
        link_to_event = self.link_obj.generate_link()
        emails = self.email_obj.get_subscriber_emails()

        message = (
            f"{self.event.name} | +{self.event.event_age}\n\n"
            f"Детальніше: {link_to_event}\n"
            f"текст"
        )

        send_mail(
            f"Нова подія від {self.creator.get_full_name()}",
            message,
            settings.EMAIL_HOST_USER,
            emails,
            fail_silently=fail_silently,
        )
