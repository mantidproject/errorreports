from django.contrib import admin

# Register your models here.
from .models import ErrorReport


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


admin.site.register(ErrorReport, ErrorAdmin)

