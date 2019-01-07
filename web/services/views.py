from services.models import ErrorReport, UserDetails, RecoveryFiles
from services.constants import input_box_max_length
from rest_framework import response, viewsets, views
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,
                                        IsAdminUser, BasePermission)
from rest_framework import status
from django.conf import settings
from django.core.files import File
from services.serializer import ErrorSerializer
import django_filters
from django.http import HttpResponse
import hashlib
import os
import pytz
from django.utils.dateparse import parse_datetime


class WithinDateFilter(django_filters.DateFilter):
    def filter(self, queryset, value):
        from datetime import timedelta
        if value:
            # date_value = value.replace(hour=0, minute=0, second=0)
            filter_lookups = {
                "%s__range" % (self.name,): (
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
            filter_lookups = {self.name: value}
            queryset = queryset.filter(**filter_lookups)
        return queryset


class ErrorFilter(django_filters.FilterSet):
    date = WithinDateFilter(name="dateTime")
    datemin = django_filters.DateFilter(name="dateTime", lookup_expr='gte')
    datemax = django_filters.DateFilter(name="dateTime", lookup_expr='lt')
    uid = MD5Filter(name="uid")
    host = MD5Filter(name="host")

    class Meta:
        model = ErrorReport
        fields = '__all__'
        order_by = ['-dateTime']


class RecoveryFileUploadView(views.APIView):
    parser_classes = (MultiPartParser, FileUploadParser)

    def get(self, request):
        return HttpResponse("Please supply recovery data as POST.")

    def post(self, request):
        up_file = request.FILES['file']
        if up_file.size > 1.049e+7:
            return Response('Provided file is too large size {}'
                            .format(up_file.size), status.HTTP_403_FORBIDDEN)
        file_hash = up_file.name.replace('.zip', '')
        corrosponding_report = RecoveryFiles. \
            objects.filter(fileHash=file_hash).count()
        if corrosponding_report:
            my_file = File(up_file)
            obj = RecoveryFiles.objects.get(fileHash=file_hash)
            obj.fileStore = my_file
            obj.save()
            return Response(up_file.name, status.HTTP_201_CREATED)
        return Response(up_file.name, status.HTTP_403_FORBIDDEN)


class RecoveryFileDownloadView(views.APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request, file_hash='No Hash Supplied'):
        if settings.MEDIA_ROOT not in os.path. \
                abspath(os.path.join(settings.MEDIA_ROOT, file_hash)):
            return Response(file_hash, status.HTTP_403_FORBIDDEN)

        path_to_file = os.path. \
            abspath(os.path.join(settings.MEDIA_ROOT, file_hash))
        if os.path.exists(path_to_file):
            zip_file = open(path_to_file, 'br')
            response = HttpResponse(zip_file,
                                    content_type='application/force-download')
            response['Content-Disposition'] \
                = 'attachment; filename="%s"' % file_hash
            return response
        return Response(path_to_file, status.HTTP_404_NOT_FOUND)


class IsAuthenticatedOrWriteOnly(BasePermission):
    """
    The request is authenticated as a user, or is a write-only request.
    """

    def has_permission(self, request, view):
        WRITE_METHODS = ["POST", ]

        return (
            request.method in WRITE_METHODS or
            request.user and
            request.user.is_authenticated()
        )


class ErrorViewSet(viewsets.ModelViewSet):
    """All errors registered in the system. Valid filter parameters are:
    'datemin' and 'datemax'.
    """
    queryset = ErrorReport.objects.all()
    serializer_class = ErrorSerializer
    permission_classes = (IsAuthenticatedOrWriteOnly,)
    filter_class = ErrorFilter

    def create(self, request):
        if request.method == 'POST':
            post_data = request.data
            self.saveErrorReport(post_data)
            return HttpResponse(status=201)
        else:
            return HttpResponse("Please supply feature error "
                                "report data as POST.")

    def saveErrorReport(self, report):
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

        if "name" in report and "email" in report:
            name = report["name"]
            name = (name[:input_box_max_length - 2] + '..') if \
                len(name) > input_box_max_length else name
            email = report["email"]
            email = (email[:input_box_max_length - 2] + '..') if \
                len(email) > input_box_max_length else email

            user, created = UserDetails.objects.get_or_create(name=name,
                                                              email=email)
            user.save()
        else:
            user = None

        if "fileHash" in report:
            fileHash = report["fileHash"]
            if fileHash:
                file_object, created = \
                    RecoveryFiles.objects.get_or_create(fileHash=fileHash)
                file_object.save()
            else:
                file_object = None
        else:
            file_object = None

        obj, created = \
            ErrorReport.objects.get_or_create(osReadable=osReadable,
                                              application=application,
                                              uid=uid, host=host,
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
                                              recoveryFile=file_object)
        if not created:
            obj.save()


@api_view(('GET',))
def api_root(request, format=None):
    return response.Response({
    })
