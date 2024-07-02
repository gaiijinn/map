from django.core.mail import send_mail
from django.conf import settings


def send_reject_event_email(event: object):
    send_mail(
        "ну кароч еткст",
        "отменка",
        f'{settings.EMAIL_HOST_USER}',
        [event.creator.email],
        fail_silently=False,
    )


def send_approved_event_email(event: object):
    send_mail(
        "ну кароч еткст",
        "ура сигма мейл",
        f'{settings.EMAIL_HOST_USER}',
        [event.creator.email],
        fail_silently=False,
    )
