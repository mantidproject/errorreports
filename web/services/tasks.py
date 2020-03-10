from django.conf import settings
import requests
import logging

logger = logging.getLogger('NotificationLogger')


def send_notification_to_slack(name,
                               email,
                               additional_text,
                               stacktrace,
                               application,
                               version,
                               os
                               ):
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
    text = """Name: {}  Email: {}
        Additional text:
        {}
        Stack Trace:
        {}
        Using: {} {} on {}
    """.format(
        name if name
        else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT,
        email if email else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT,
        additional_text if additional_text
        else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT,
        stacktrace if stacktrace
        else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT,
        application if application
        else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT,
        version if version
        else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT,
        os if os
        else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT)
    requests.post(slack_webhook_url,
                  json={
                      'channel': settings.SLACK_ERROR_REPORTS_CHANNEL,
                      'username': settings.SLACK_ERROR_REPORTS_USERNAME,
                      'text': text,
                      'icon_emoji': settings.SLACK_ERROR_REPORTS_EMOJI
                  })


def send_logging_output_to_slack(message):
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    if slack_webhook_url is None:
        return
    requests.post(slack_webhook_url,
                  json={
                      'channel': settings.SLACK_SERVER_ERRORS_CHANNEL,
                      'username': settings.SLACK_ERROR_REPORTS_USERNAME,
                      'text': message,
                      'icon_emoji': settings.SLACK_ERROR_REPORTS_EMOJI
                  })
