from services.models import ErrorReport, UserDetails
from services.utils.github_issue_manager import get_or_create_github_issue
from services.constants import input_box_max_length
from rest_framework import response, viewsets, views
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from services.serializer import ErrorSerializer
import django_filters
from django.http import HttpResponse
import hashlib
import pytz
from django.utils.dateparse import parse_datetime
import logging

logger = logging.getLogger("django")
RECOVERY_FILE_SIZE_MAX_BYTES = 10 * 1024 * 1024


class WithinDateFilter(django_filters.DateFilter):
    def filter(self, queryset, value):
        from datetime import timedelta

        if value:
            # date_value = value.replace(hour=0, minute=0, second=0)
            filter_lookups = {
                "%s__range" % (self.field_name,): (
                    value,
                    value + timedelta(days=1),
                ),
            }
            queryset = queryset.filter(**filter_lookups)
        return queryset


class MD5Filter(django_filters.CharFilter):
    def filter(self, queryset, value):
        if value:
            if len(value) != 32:
                value = hashlib.md5(value).hexdigest()
            filter_lookups = {self.field_name: value}
            queryset = queryset.filter(**filter_lookups)
        return queryset


class ErrorFilter(django_filters.FilterSet):
    date = WithinDateFilter(field_name="dateTime")
    datemin = django_filters.DateFilter(field_name="dateTime", lookup_expr="gte")
    datemax = django_filters.DateFilter(field_name="dateTime", lookup_expr="lt")
    uid = MD5Filter(field_name="uid")
    host = MD5Filter(field_name="host")

    class Meta:
        model = ErrorReport
        fields = "__all__"
        order_by = ["-dateTime"]


class RecoveryFileUploadView(views.APIView):
    def get(self, request):
        return HttpResponse("Error Reports no longer accept Recovery Files.")

    def post(self, request):
        return Response(
            "Error Reports no longer accept Recovery Files.", status.HTTP_201_CREATED
        )


class IsAuthenticatedOrWriteOnly(BasePermission):
    """
    The request is authenticated as a user, or is a write-only request.
    """

    def has_permission(self, request, view):
        WRITE_METHODS = [
            "POST",
        ]

        return (
            request.method in WRITE_METHODS
            or request.user
            and request.user.is_authenticated
        )


def saveErrorReport(report):
    osReadable = report["osReadable"]
    application = report["application"]
    uid = report["uid"]
    host = report["host"]
    dateTime = parse_datetime(report["dateTime"])
    if dateTime.tzinfo is None:
        dateTime = pytz.timezone("UTC").localize(dateTime)
    osName = report["osName"]
    osArch = report["osArch"]
    osVersion = report["osVersion"]
    ParaView = report["ParaView"]
    mantidVersion = report["mantidVersion"]
    mantidSha1 = report["mantidSha1"]
    facility = report["facility"]
    upTime = report["upTime"]
    exitCode = report["exitCode"]
    textBox = report["textBox"] if "textBox" in report else ""
    stacktrace = report["stacktrace"] if "stacktrace" in report else ""
    cppCompressedTraces = (
        report["cppCompressedTraces"] if "cppCompressedTraces" in report else ""
    )

    if "name" in report and "email" in report:
        name = report["name"]
        name = (
            (name[: input_box_max_length - 2] + "..")
            if len(name) > input_box_max_length
            else name
        )
        email = report["email"]
        email = (
            (email[: input_box_max_length - 2] + "..")
            if len(email) > input_box_max_length
            else email
        )

        user, created = UserDetails.objects.get_or_create(name=name, email=email)
        user.save()
    else:
        user = None

    github_issue = get_or_create_github_issue(report)

    obj, created = ErrorReport.objects.get_or_create(
        osReadable=osReadable,
        application=application,
        uid=uid,
        host=host,
        dateTime=dateTime,
        osName=osName,
        osArch=osArch,
        osVersion=osVersion,
        ParaView=ParaView,
        mantidVersion=mantidVersion,
        mantidSha1=mantidSha1,
        facility=facility,
        upTime=upTime,
        exitCode=exitCode,
        user=user,
        textBox=textBox,
        stacktrace=stacktrace,
        cppCompressedTraces=cppCompressedTraces,
        githubIssue=github_issue,
    )
    if not created:
        obj.save()


class ErrorViewSet(viewsets.ModelViewSet):
    """All errors registered in the system. Valid filter parameters are:
    'datemin' and 'datemax'.
    """

    queryset = ErrorReport.objects.all()
    serializer_class = ErrorSerializer
    permission_classes = (IsAuthenticatedOrWriteOnly,)
    filter_class = ErrorFilter

    def create(self, request):
        if request.method == "POST":
            post_data = request.data
            saveErrorReport(post_data)
            return HttpResponse(status=201)
        else:
            return HttpResponse("Please supply feature error report data as POST.")


@api_view(("GET",))
def api_root(request, format=None):
    return response.Response({})
