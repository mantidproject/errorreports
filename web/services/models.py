from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import signals
from services.tasks import send_notification_to_slack
from services.constants import input_box_max_length, free_text_max_length
from services.utils.handel_compressed_cpp_traces import (
    extract_mantid_code_threads_from_cpp_traces
)
import logging
import threading


logger = logging.getLogger("Error report model")
# Implements saving recovery files to disk
FILE_SYSTEM_STORE = FileSystemStorage(location=settings.MEDIA_ROOT)

# Fixed constants used when system is tested
TEST_VALUES = ('public_email', 'Not provided', '', 'Something went wrong')


class ErrorReport(models.Model):
    # md5 ex: "c5a9b601408709f47417bcba3571262b"
    uid = models.CharField(max_length=32, help_text="md5 version of username")
    # md5 ex: "7defb184ceadab4e79eff323359ad373"
    host = models.CharField(max_length=32, help_text="md5 version of hostname")
    # ex: "2014-12-08T18:50:35.817942000"
    dateTime = models.DateTimeField(db_index=True)
    osName = models.CharField(max_length=32)  # ex: "Linux"
    osArch = models.CharField(max_length=16)  # ex: "x86_64"
    # ex: "3.17.4-200.fc20.x86_64"
    osVersion = models.CharField(max_length=32)
    ParaView = models.CharField(max_length=16)  # ex: "3.98.1"
    mantidVersion = models.CharField(max_length=64)  # ex: "3.2.20141208.1820"
    # sha1 ex: "e9423bdb34b07213a69caa90913e40307c17c6cc"
    mantidSha1 = models.CharField(max_length=40,
                                  help_text="sha1 for specific mantid version")
    # ex: "Fedora 20 (Heisenbug)"
    osReadable = models.CharField(max_length=80, default="", blank=True)
    application = models.CharField(max_length=80, default="", blank=True)

    facility = models.CharField(max_length=32, default="", blank=True)
    exitCode = models.CharField(max_length=32,
                                default="",
                                null=True,
                                blank=True)
    upTime = models.CharField(max_length=32, default="")
    user = models.ForeignKey('UserDetails',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)
    textBox = models.CharField(max_length=free_text_max_length,
                               default="",
                               null="True")
    stacktrace = models.CharField(max_length=10000, default="")
    cppCompressedTraces = models.CharField(max_length=10000, default="",
                                           blank=True)
    githubIssue = models.ForeignKey('GithubIssue',
                                    on_delete=models.SET_NULL,
                                    blank=True,
                                    null=True)

    def removePIIData(reports):
        # Delete identifiable parts of chosen reports
        reports.update(uid="")
        reports.update(host="")
        reports.update(user_id="")
        reports.update(textBox="")
        reports.update(stacktrace="")

        UserDetails.clearOrphanedRecords()


class UserDetails(models.Model):
    name = models.CharField(max_length=input_box_max_length,
                            help_text="user provided name")
    email = models.CharField(max_length=input_box_max_length,
                             help_text="user provided email")

    def clearOrphanedRecords():
        # First sort all UserDetailRecords by their
        # Foreign Key count "errorreport", then using a named pipe
        # Filter out all records equal to 0
        no_refs = UserDetails.objects.annotate(
            num_refs=models.Count('errorreport')).filter(num_refs=0)
        no_refs.delete()


class GithubIssue(models.Model):
    repoName = models.CharField(max_length=200,
                                default="",
                                blank=True,
                                help_text="'user/repo_name': for example "
                                          "'mantidproject/mantid'")
    issueNumber = models.CharField(max_length=16, default="", blank=True)


def notify_report_received(sender, instance, signal, *args, **kwargs):
    """
    Send a notification to the defined endpoint when a new error
    report is received
    :param sender: Unused
    :param instance: The instance of ErrorReport that caused to notification
    :param signal: Unused
    :param args: Unused
    :param kwargs: Unused
    """
    textBox = instance.textBox
    stacktrace = instance.stacktrace

    if instance.cppCompressedTraces != "":
        stacktrace = "\n\n".join(extract_mantid_code_threads_from_cpp_traces(
                                 instance.cppCompressedTraces))

    if instance.user is None:

        if ((stacktrace in TEST_VALUES
             and textBox in TEST_VALUES)):
            return
        else:
            name = "Not provided"
            email = "Not provided"

    else:
        name = instance.user.name
        email = instance.user.email

    # Don't send a slack notification if there was not
    # a useful email, stacktrace or text provided
    # as we can't actively do anything about it
    if ((email in TEST_VALUES
         and stacktrace in TEST_VALUES
         and textBox in TEST_VALUES)):
        return

    issue_link = ""
    if instance.githubIssue:
        issue_link = (f"https://github.com/{instance.githubIssue.repoName}"
                      f"/issues/{instance.githubIssue.issueNumber}")

    notification_thread = threading.Thread(
        target=send_notification_to_slack, args=(name,
                                                 email,
                                                 instance.textBox,
                                                 stacktrace,
                                                 instance.application,
                                                 instance.mantidVersion,
                                                 instance.osReadable,
                                                 issue_link))
    notification_thread.start()


signals.post_save.connect(notify_report_received, sender=ErrorReport)
