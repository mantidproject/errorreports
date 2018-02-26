from rest_framework import serializers
from .models import ErrorReport, UserDetails


class ErrorSerializer(serializers.HyperlinkedModelSerializer):
    # use everything, but the following are optional
    osReadable = serializers.CharField(required=False, allow_blank=True)
    application = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ErrorReport
        # fields = '__all__'
        fields = ['osReadable', 'application', 'url', 'uid',
                  'host', 'dateTime', 'osName', 'osArch', 'osVersion',
                  'ParaView', 'mantidVersion', 'mantidSha1', 'facility',
                  'exitCode', 'upTime']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserDetails
        fields = ['name', 'email', 'dateTime']
        