from django.db import models
from services.constants import input_box_max_length, free_text_max_length
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models import signals
from celery_app.tasks import send_notification_email

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


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
    mantidSha1 = models.CharField(
        max_length=40, help_text="sha1 for specific mantid version")
    # ex: "Fedora 20 (Heisenbug)"
    osReadable = models.CharField(max_length=80, default="", blank=True)
    application = models.CharField(max_length=80, default="", blank=True)

    facility = models.CharField(max_length=32, default="", blank=True)
    exitCode = models.CharField(max_length=32, default="",
                                null=True, blank=True)
    upTime = models.CharField(max_length=32, default="")
    user = models.ForeignKey('UserDetails', on_delete=models.SET_NULL,
                             blank=True, null=True)
    textBox = models.CharField(max_length=free_text_max_length, default="",
                               null="True")
    recoveryFile = models.ForeignKey('RecoveryFiles',
                                     on_delete=models.SET_NULL,
                                     blank=True, null=True)


class UserDetails(models.Model):
    name = models.CharField(max_length=input_box_max_length,
                            help_text="user provided name")
    email = models.CharField(max_length=input_box_max_length,
                             help_text="user provided email")


class RecoveryFiles(models.Model):
    fileHash = models.CharField(max_length=32,
                                help_text="md5 name of recovery file",
                                default='')
    fileStore = models.FileField(storage=fs, null=True,
                                 validators=[FileExtensionValidator(
                                     allowed_extensions=['zip'])])


def send_email_notification(sender, instance, signal, *args, **kwargs):
    name = instance.user.name if instance.user else ''
    email = instance.user.email if instance.user else ''
    text_box = instance.textBox
    if name or email or text_box:
        send_notification_email.delay(name, email, text_box)


signals.post_save.connect(send_email_notification, sender=ErrorReport)
