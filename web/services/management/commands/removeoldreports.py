from django.core.management.base import BaseCommand
from services.models import ErrorReport, UserDetails
from datetime import timedelta
from django.utils import timezone

DEFAULT_RECOVERY_FILE_AGE_DAYS = 90


class Command(BaseCommand):
    help = 'Deletes all ErrorReports (over 90 days old by default),\
        and removes UserDetails not related to any active reports. '

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

        for report in reports:
            # Delete chosen reports
            report.delete()

        """Get UserDetails which are not tied to any surviving ErrorReports"""

        users_with_surviving_reports = ErrorReport.objects.exclude(
                dateTime__lte=timezone.now()-timedelta(days=options['days'])
                ).values_list('user')

        active_users = []  # User IDs with surviving reports
        all_user = UserDetails.objects.all()  # All UserDetails objects
        all_user_list = []  # All User IDs
        empty_users = []  # User IDs with NO surviving reports
        empty_users_objects = []  # UserDetails objects
        #                           with NO surviving reports

        # Get a list of User IDs for all active/surviving reports
        for i in range(len(users_with_surviving_reports)):
            (Active_User_ID,) = users_with_surviving_reports[i]
            if Active_User_ID is not None:
                active_users.append(Active_User_ID)

        # Get lists of User Objects and IDs,
        # with NO active/surviving error reports
        for index in range(len(all_user)):
            (User_ID,) = all_user.values_list('id')[index]
            all_user_list.append(User_ID)
            if all_user_list[index] not in active_users:
                empty_users_objects.append(all_user[index])
                empty_users.append(User_ID)

        # Print User IDs for deleting
        print("Active Users:")
        print(active_users)
        print("All Users:")
        print(all_user_list)
        print("Deleting Details of Empty Users:")
        print(empty_users)
        print('Deleting UserDetails Objects:')
        print(empty_users_objects)

        for user_details in empty_users_objects:
            # Delete UserDetails with no reports
            user_details.delete()
