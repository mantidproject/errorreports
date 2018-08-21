from services.models import ErrorReport, UserDetails
from services.constants import input_box_max_length
from rest_framework import response, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from services.serializer import ErrorSerializer
import django_filters
from django.http import HttpResponse
import json
import hashlib


class WithinDateFilter(django_filters.DateFilter):
    def filter(self, queryset, value):
        from datetime import timedelta
        if value:
            # date_value = value.replace(hour=0, minute=0, second=0)
            filter_lookups = {
                "%s__range" % (self.name, ): (
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


class ErrorViewSet(viewsets.ModelViewSet):
    """All errors registered in the system. Valid filter parameters are:
    'host', 'uid', 'datemin', 'datemax', and 'date'.
    """
    queryset = ErrorReport.objects.all()
    serializer_class = ErrorSerializer
    permission_classes = [AllowAny]
    filter_class = ErrorFilter

    def create(self, request):
        if request.method == 'POST':
            post_data = json.loads(request.body)
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
        dateTime = report["dateTime"]
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
            name = (name[:input_box_max_length-2] + '..') if\
                len(name) > input_box_max_length else name
            email = report["email"]
            email = (email[:input_box_max_length-2] + '..') if\
                len(email) > input_box_max_length else email
            if UserDetails.objects.filter(email=email).exists():
                user = UserDetails.objects.get(email=email)
            else:
                user, created = UserDetails.objects.get_or_create(name=name,
                                                                  email=email)
            user.save()
        else:
            user = None

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
                                              textBox=textBox)
        obj.save()


@api_view(('GET',))
def api_root(request, format=None):
    return response.Response({
    })
