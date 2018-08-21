from django.contrib import admin

# Register your models here.
from .models import ErrorReport, UserDetails


class ErrorAdmin(admin.ModelAdmin):
    list_display = ('uid',
                    'host',
                    'dateTime',
                    'osName',
                    'osArch',
                    'osReadable',
                    'osVersion',
                    'ParaView',
                    'mantidVersion',
                    'mantidSha1',
                    'application',
                    'facility',
                    'exitCode',
                    'upTime',
                    'textBox',
                    'get_user_email')

    def get_user_email(self, obj):
        return obj.user.email
    get_user_email.admin_order_field = 'email'
    get_user_email.short_description = 'User provided email'


class UserAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'email')


admin.site.register(ErrorReport, ErrorAdmin)
admin.site.register(UserDetails, UserAdmin)
