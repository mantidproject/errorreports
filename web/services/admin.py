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
                    'upTime')

class UserAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'email',
                    'dateTime')


admin.site.register(ErrorReport, ErrorAdmin)
admin.site.register(UserDetails, UserAdmin)

