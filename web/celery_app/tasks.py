from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings


@shared_task
def send_notification_email(name, email, text_box):
    to_address = [settings.EMAIL_TO_ADDRESS]
    from_address = settings.EMAIL_FROM_ADDRESS
    subject = 'User error report'

    message = (
        'An error report has been submitted by {}'
        ' who provided the following email {}. '
        '\nThe following information was sent:\n\n {}'
        '\n'
        '\n https://errorreports.mantidproject.org/admin/'
    ).format(name, email, text_box)

    send_mail(subject,
              message,
              from_address,
              to_address,
              fail_silently=False,
              )


@shared_task
def hello():
    print('Hello there')
