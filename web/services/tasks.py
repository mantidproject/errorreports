from django.conf import settings
import requests
import logging
from string import Template

logger = logging.getLogger("NotificationLogger")
SLACK_MESSAGE = Template("""
Name: $name Email: $email
Facility: $facility
Additional text:
$add_text
Using: $application $version on $os
Issue link: $issue_link
Exit code: $exit_code
Stack Trace:
""")


def send_notification_to_slack(
    name,
    email,
    facility,
    additional_text,
    stacktrace,
    exit_code,
    application,
    version,
    os,
    github_issue_link,
):
    """Sends a notification about a new error report to the slack
    channel defined in the settings

    :param name: The name field supplied in the error report
    :param email: The email address supplied in the error report.
                  This is required.
    :param facility: The facility where the error occurred.
    :param additional_text: Any additional text provided by the user.
    :param exit_code: The exit code provided.
    :param application: The application where the error occurred.
    :param version: The version of the application.
    :param os: The operating system where the error occurred.
    :param github_issue_link: The link to the GitHub issue for this error.
    """
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    if not slack_webhook_url:
        return
    text = SLACK_MESSAGE.substitute(
        name=_string_or_empty_field(name),
        email=_string_or_empty_field(email),
        facility=_string_or_empty_field(facility),
        add_text=_string_or_empty_field(additional_text),
        application=_string_or_empty_field(application),
        version=_string_or_empty_field(version),
        os=_string_or_empty_field(os),
        issue_link=github_issue_link,
        exit_code=_string_or_empty_field(exit_code),
    )
    stacktrace_text = f"```{_string_or_empty_field(stacktrace)}```"
    requests.post(
        slack_webhook_url,
        json={
            "channel": settings.SLACK_ERROR_REPORTS_CHANNEL,
            "username": settings.SLACK_ERROR_REPORTS_USERNAME,
            "text": text,
            "icon_emoji": settings.SLACK_ERROR_REPORTS_EMOJI,
            "attachments": [{"mrkdwn_in": ["text"], "text": stacktrace_text}],
        },
    )


def _string_or_empty_field(value: str):
    return value if value else settings.SLACK_ERROR_REPORTS_EMPTY_FIELD_TEXT


def send_logging_output_to_slack(message):
    slack_webhook_url = settings.SLACK_WEBHOOK_URL
    if not slack_webhook_url:
        return
    requests.post(
        slack_webhook_url,
        json={
            "channel": settings.SLACK_SERVER_ERRORS_CHANNEL,
            "username": settings.SLACK_ERROR_REPORTS_USERNAME,
            "text": message,
            "icon_emoji": settings.SLACK_ERROR_REPORTS_EMOJI,
        },
    )
