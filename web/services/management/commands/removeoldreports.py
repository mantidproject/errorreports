from django.core.management.base import BaseCommand
from services.models import ErrorReport
from datetime import timedelta
from django.utils import timezone

DEFAULT_RECOVERY_FILE_AGE_DAYS = 90


class Command(BaseCommand):
    help = 'Removes identifiable information from ErrorReports (over 90 days \
            old by default), and removes UserDetails \
            not related to any active reports. '

    def add_arguments(self, parser):
        parser.add_argument('--all',
                            action='store_true',
                            dest='all',
                            help='remove all reports and user details')

        parser.add_argument('days', type=int, nargs='?',
                            help='Number of days to save',
                            default=DEFAULT_RECOVERY_FILE_AGE_DAYS)

    def handle(self, *args, **options):

        """Get All or Old reports and delete them"""

        all_reports = ErrorReport.objects.all()

        if options['all']:
            # Choose all reports
            reports = all_reports

        else:
            # Choose reports older than a number of days, 90 by default
            reports = ErrorReport.objects.filter(
                dateTime__lte=timezone.now()-timedelta(days=options['days']))

        # empties reports and removes orphaned user details
        ErrorReport.removePIIData(reports)
