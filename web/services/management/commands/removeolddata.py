from django.core.management.base import BaseCommand
from services.models import ErrorReport
from datetime import timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = 'Deletes all recovery files over a month old'

    def handle(self, *args, **options):
        reports = ErrorReport.objects.filter(
            dateTime__lte=timezone.now() - timedelta(days=30)).filter(
            recoveryFile__isnull=False)

        for report in reports:
            report.recoveryFile.fileStore.delete(save=False)
            report.recoveryFile.delete()
