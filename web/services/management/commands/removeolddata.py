from django.core.management.base import BaseCommand
from services.models import ErrorReport
from datetime import timedelta
from django.utils import timezone

DEFAULT_RECOVERY_FILE_AGE_DAYS = 30


class Command(BaseCommand):
    help = 'Deletes all recovery files over a month old'

    def add_arguments(self, parser):
        parser.add_argument('--all',
                            action='store_true',
                            dest='all', help='remove all files')

        parser.add_argument('days', type=int, nargs='?',
                            help='Number of days to save',
                            default=DEFAULT_RECOVERY_FILE_AGE_DAYS)

    def handle(self, *args, **options):
        if options['all']:
            reports = ErrorReport.objects.filter(
                recoveryFile__isnull=False)
        else:
            reports = ErrorReport.objects.filter(
                dateTime__lte=timezone.now()-timedelta(days=options['days']))\
                .filter(recoveryFile__isnull=False)

        for report in reports:
            report.recoveryFile.fileStore.delete(save=False)
            report.recoveryFile.delete()
