from django.contrib import admin
# Register your models here.
from services.models import ErrorReport, UserDetails


class ErrorAdmin(admin.ModelAdmin):
    list_display = (
                    'dateTime',
                    'osReadable',
                    'ParaView',
                    'mantidVersion',
                    'mantidSha1',
                    'application',
                    'facility',
                    'exitCode',
                    'upTime',
                    'textBox',
                    'get_user_email',
                    'stacktrace')

    def get_user_email(self, obj):
        return obj.user.email if obj.user else ''
    get_user_email.admin_order_field = 'user__email'
    get_user_email.short_description = 'User provided email'


class UserAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'email')


admin.site.register(ErrorReport, ErrorAdmin)
admin.site.register(UserDetails, UserAdmin)
