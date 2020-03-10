from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models import signals
from services.tasks import send_notification_to_slack
from services.constants import input_box_max_length, free_text_max_length
import threading
# Implements saving recovery files to disk
FILE_SYSTEM_STORE = FileSystemStorage(location=settings.MEDIA_ROOT)

# Fixed constants used when system is tested
TEST_EMAIL = 'public_email'


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
    mantidVersion = models.CharField(max_length=32)  # ex: "3.2.20141208.1820"
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


class UserDetails(models.Model):
    name = models.CharField(max_length=input_box_max_length,
                            help_text="user provided name")
    email = models.CharField(max_length=input_box_max_length,
                             help_text="user provided email")


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
    if instance.user is None:
        return

    email = instance.user.email
    if email == TEST_EMAIL:
        # Don't send a notification if there was not email provided as we can't
        # actively do anything about it
        return
    notification_thread = threading.Thread(target=send_notification_to_slack, args=(instance.user.name,
                               email,
                               instance.textBox,
                               instance.stacktrace,
                               instance.application,
                               instance.mantidVersion,
                               instance.osReadable))
    notification_thread.start()

signals.post_save.connect(notify_report_received, sender=ErrorReport)
