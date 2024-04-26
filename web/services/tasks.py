from django.conf import settings
import requests
import logging
from string import Template

logger = logging.getLogger('NotificationLogger')
slack_message = Template("""
Name: $name Email: $email
Additional text:
$add_text
Stack Trace:
$stacktrace
Using: $application $version on $os
$issue_link
""")


def send_notification_to_slack(name,
                               email,
                               additional_text,
                               stacktrace,
                               application,
                               version,
                               os,
                               github_issue_link
                               ):
    """Sends a notification about a new error report to the slack
    channel defined in the settings

    :param name: The name field supplied in the error report
    :param email: The email address supplied in the error report.
                  This is required.
    :param additional_text: Any additional text provided
    """
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    if not slack_webhook_url:
        return
    text = slack_message.substitute(
        name=_string_or_empty_field(name),
        email=_string_or_empty_field(name),
        add_text=_string_or_empty_field(additional_text),
        stacktrace=_string_or_empty_field(stacktrace),
        application=_string_or_empty_field(application),
        version=_string_or_empty_field(version),
        os=_string_or_empty_field(os),
        issue_link=_string_or_empty_field(github_issue_link)
    )
    requests.post(slack_webhook_url,
                  json={
                      'channel': settings.SLACK_ERROR_REPORTS_CHANNEL,
                      'username': settings.SLACK_ERROR_REPORTS_USERNAME,
                      'text': text,
                      'icon_emoji': settings.SLACK_ERROR_REPORTS_EMOJI
                  })


def _string_or_empty_field(value: str):
    return value if value else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT


def send_logging_output_to_slack(message):
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    if not slack_webhook_url:
        return
    requests.post(slack_webhook_url,
                  json={
                      'channel': settings.SLACK_SERVER_ERRORS_CHANNEL,
                      'username': settings.SLACK_ERROR_REPORTS_USERNAME,
                      'text': message,
                      'icon_emoji': settings.SLACK_ERROR_REPORTS_EMOJI
                  })
