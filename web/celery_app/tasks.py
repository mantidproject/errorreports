from django.conf import settings
import requests

from celery import shared_task


@shared_task
def send_notification_to_slack(name, email, additional_text):
    """Sends a notification about a new error report to the slack
    channel defined in the settings

    :param name: The name field supplied in the error report
    :param email: The email address supplied in the error report.
                  This is required.
    :param additional_text: Any additional text provided
    """
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    if slack_webhook_url is None:
        return
    text = """An error report was received. Details:
        Name: {}
        Email: {}
        Additional text:
        {}
    """.format(
        name if name else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT, email,
        additional_text
        if additional_text else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT)
    requests.post(slack_webhook_url,
                  json={
                      'channel': settings.SLACK_ERROR_REPORTS_CHANNEL,
                      'username': settings.SLACK_ERROR_REPORTS_USERNAME,
                      'text': text,
                      'icon_emoji': settings.SLACK_ERROR_REPORTS_EMOJI
                  })
