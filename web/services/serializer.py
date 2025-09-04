from rest_framework import serializers
from .models import ErrorReport


class ErrorSerializer(serializers.HyperlinkedModelSerializer):
    # use everything, but the following are optional
    osReadable = serializers.CharField(required=False, allow_blank=True)
    application = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = ErrorReport

        fields = [
            "osReadable",
            "application",
            "url",
            "uid",
            "host",
            "dateTime",
            "osName",
            "osArch",
            "osVersion",
            "ParaView",
            "mantidVersion",
            "mantidSha1",
            "facility",
            "exitCode",
            "upTime",
            "textBox",
            "stacktrace",
            "cppCompressedTraces",
            "name",
            "email",
        ]
