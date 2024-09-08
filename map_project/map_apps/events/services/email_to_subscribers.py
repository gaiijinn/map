from abc import ABC, abstractmethod

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


class BaseSubscriberEmailGetter(ABC):
    @abstractmethod
    def get_subscriber_emails(self, creator_obj):
        pass


class SubscriberEmailGetter(BaseSubscriberEmailGetter):
    def get_subscriber_emails(self, creator_obj):
        subscribers = creator_obj.subscriptions_received.all()
        emails = [subscription.user.email for subscription in subscribers]
        return emails


class EventLinkGenerator:
    def generate_link(self, event_obj):
        host = f"{settings.DOMAIN_NAME}:{settings.PORT}"
        event_url = reverse("events:events-detail", kwargs={'pk': event_obj.id})

        return f"{host}{event_url}"


class EmailToSubscribers:
    def __init__(self, event_obj):
        self.event = event_obj
        self.creator = event_obj.creator

        self.email_obj = SubscriberEmailGetter().get_subscriber_emails(self.creator)
        self.link_obj = EventLinkGenerator().generate_link(self.event)

    def send_email(self):
        message = (
            f"{self.event.name} | +{self.event.event_age}\n\n"
            f"Детальніше: {self.link_obj}\n"
            f"текст"
        )

        send_mail(
            f"Нова подія від {self.creator.get_full_name()}",
            message,
            settings.EMAIL_HOST_USER,
            self.email_obj,
            fail_silently=True,
        )
