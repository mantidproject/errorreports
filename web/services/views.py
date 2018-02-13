from django.shortcuts import render

# # Create your views here.
from django.views.decorators.cache import cache_page
from services.models import ErrorReport
from rest_framework import response, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from services.serializer import ErrorSerializer
import django_filters
from rest_framework.reverse import reverse
from django.http import HttpResponse
import json
import datetime
import hashlib
import settings

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
            return HttpResponse("Please supply feature error report data as POST.")

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

        obj, created = ErrorReport.objects.get_or_create(osReadable=osReadable,
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
                                                   exitCode=exitCode)
        obj.save()


def filterByDate(queryset, request=None, datemin=None, datemax=None):
    if request:
        datemin = request.GET.get("datemin", datemin)
        datemax = request.GET.get("datemax", datemax)
        # datemax = request.data.get("datemax", datemax)
        # datemax = request.data.get("datemax", datemax)

    if datemin:
        queryset = django_filters.DateFilter(
            name="dateTime", lookup_expr='gte').filter(queryset, datemin)

    if datemax:
        queryset = django_filters.DateFilter(
            name="dateTime", lookup_expr='lt').filter(queryset, datemax)

    return (queryset, datemin, datemax)


def parseDate(date):
    date = date.split('-')
    date = [int(i) for i in date]
    date = datetime.date(*date)
    return date


def getDateRange(queryset, datemin=None, datemax=None):
    queryset = queryset.order_by("dateTime")
    dates = []
    delta = datetime.timedelta(days=1)
    if datemin:
        item = parseDate(datemin)
    else:
        item = queryset.first().dateTime.date()
    if datemax:
        end = parseDate(datemax)
    else:
        end = queryset.last().dateTime.date()
    while item <= end:
        dates.append(item)
        item += delta
    return dates


def prepResult(dates):
    result = {'date': dates, 'total': [], 'other': []}
    for label in OS_NAMES:
        result[label] = []
    return result


def convertResult(result):
    mapping = {'Linux': 'linux', 'Darwin': 'mac', 'Windows NT': 'windows'}
    for key in mapping.keys():
        if key in result:
            result[mapping[key]] = result.pop(key)
    return result


def error_by_field(request, format=None, field=None):
    (queryset, datemin, datemax) = filterByDate(Usage.objects.all(), request)
    dates = getDateRange(queryset, datemin, datemax)
    result = prepResult(dates)

    dateFilter = WithinDateFilter('dateTime')
    for date in dates:
        queryset_date = dateFilter.filter(queryset, date)
        total = query_count(queryset_date, field)
        cumulative = 0
        for label in OS_NAMES:
            count = query_count(queryset_date.filter(osName=label), field)
            cumulative += count
            result[label].append(count)
        result['total'].append(total)
        # one user can be on multiple systems
        result['other'].append(max(0, total - cumulative))

    result = convertResult(result)

    # make the result look like a d3.csv load
    finalResult = []
    for i in range(len(result['date'])):
        line = {}
        for key in result.keys():
            line[key] = result[key][i]
        finalResult.append(line)

    return response.Response(finalResult)


@api_view(('GET',))
def api_root(request, format=None):
    return response.Response({
        # 'by':       reverse('by-root',    request=request, format=format),
        # 'host':     reverse('host-list',  request=request, format=format),
        # 'usage':    reverse('usage-list', request=request, format=format),
        # 'user':     reverse('user-list',  request=request, format=format),
        # 'feature':  reverse('featureusage-list', request=request, format=format),
        # 'location': reverse('location-list',  request=request, format=format)
    })


# @api_view(('GET',))
# def by_root(request, format=None):
#     return response.Response({
#         'host': reverse('by-hosts', request=request, format=format),
#         'user': reverse('by-users', request=request, format=format),
#         'start': reverse('by-starts', request=request, format=format),
#     })


# @cache_page(60*30)  # half-hour cache
# def usage_plots(request, md5):
#     barGraph = plotsfile.usages_barGraph()
#     years = plotsfile.yearLinks()
#     util = plotsfile.utilLinks()
#     context = {"title": "Total Startups",
#                "bar": barGraph,
#                "years": years,
#                "util": util,
#                "goback": "<a href='/uid/'>Switch to Users</a>"}
#     return render(request, 'plots.html', context=context)


# @cache_page(60*30)  # half-hour cache
# def usage_year(request, md5, year):
#     pie = plotsfile.usages_pieChart(year)
#     map = plotsfile.usages_mapGraph(year)
#     context = {"title": "Startups By Year",
#                "pie": pie,
#                "map": map,
#                "goback": "<a href='../'>Go Back</a>"}
#     return render(request, 'plots.html', context=context)


# @cache_page(60*30)  # half-hour cache
# def uid_plots(request, md5):
#     barGraph = plotsfile.uids_barGraph()
#     years = plotsfile.yearLinks()
#     util = plotsfile.utilLinks()
#     context = {"title": "Startups By User",
#                "bar": barGraph,
#                "years": years,
#                "util": util,
#                "goback": "<a href='/usage/'>Switch to Usages</a>"}
#     return render(request, 'plots.html', context=context)


# @cache_page(60*30)  # half-hour cache
# def uid_year(request, md5, year):
#     pie = plotsfile.uids_pieChart(year)
#     map = plotsfile.uids_mapGraph(year)
#     context = {"title": "Startups By User",
#                "pie": pie,
#                "map": map,
#                "goback": "<a href='../'>Go Back</a>"}
#     return render(request, 'plots.html', context=context)
