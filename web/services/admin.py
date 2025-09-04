from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.
from services.models import ErrorReport, UserDetails


class ErrorAdmin(admin.ModelAdmin):
    list_display = (
        "dateTime",
        "osReadable",
        "ParaView",
        "mantidVersion",
        "mantidSha1",
        "application",
        "facility",
        "exitCode",
        "upTime",
        "textBox",
        "user_link",
        "stacktrace",
    )

    def user_link(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:services_userdetails_change", args=(obj.user.pk,)),
                obj.user.email,
            )
        )

    user_link.short_description = "User"


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "email")


admin.site.register(ErrorReport, ErrorAdmin)
admin.site.register(UserDetails, UserAdmin)
