from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html
# Register your models here.
from .models import ErrorReport, UserDetails, RecoveryFiles
from django.conf import settings


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
                    'get_recoveryFile')

    def get_user_email(self, obj):
        return obj.user.email if obj.user else ''
    get_user_email.admin_order_field = 'user__email'
    get_user_email.short_description = 'User provided email'

    def get_recoveryFile(self, obj):
        if obj.recoveryFile:
            link = '{}{}'.format(settings.MEDIA_URL, obj.recoveryFile.fileStore)
            return format_html('<a href="{}">{}</a>', link, obj.recoveryFile.fileStore)
        else: 
            return ''
    get_recoveryFile.short_description = 'Recovery File'


class UserAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'email')

class FilesAdmin(admin.ModelAdmin):
    list_display = ('fileHash', 'fileStore')


admin.site.register(ErrorReport, ErrorAdmin)
admin.site.register(UserDetails, UserAdmin)
admin.site.register(RecoveryFiles, FilesAdmin)
