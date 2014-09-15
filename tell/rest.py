from listen.models import Logger, Entry
from rest_framework import serializers, viewsets


class LoggerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Logger
        fields = ('id', 'name', 'regex')


class LoggerViewSet(viewsets.ModelViewSet):
    queryset = Logger.objects.all()
    serializer_class = LoggerSerializer


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
        fields = ('logger', 'data')


class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer