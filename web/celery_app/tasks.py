from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings


@shared_task
def send_notification_email(name, email, text_box):
    to_address = [settings.ERROR_EMAIL]
    subject = 'User error report'

    message = (
        'An error report has been submitted by {}'
        ' who provided the following email {}. The '
        'following information was sent {}'
    ).format(name, email, text_box)

    send_mail(subject,
              message,
              'mantidproject@gmail.com',
              to_address,
              fail_silently=False,
              )


@shared_task
def hello():
    print('Hello there')
