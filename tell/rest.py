from listen.models import Logger, Entry
from rest_framework import serializers, viewsets
import listen.net

class LoggerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Logger
        fields = ('id', 'name', 'ip_address', 'regex', 'is_active')

    is_active = serializers.SerializerMethodField('isActive')

    def isActive(self, logger):
        return logger.id in listen.net.listen_client.getStatusInformation()


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