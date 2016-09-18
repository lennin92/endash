from dashboard.models import Measure, Node, TariffSchedule
from rest_framework import serializers


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('id', 'url', 'padre', 'nombre', 'coordenada',
                  'descripcion', 'hijos', 'fotografia', 'demandas')


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measure
        fields =('node', 'datetime', 'datetime_int', 'active',
                 'apparent', 'demand')


class TariffScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TariffSchedule
        fields = (
            'supplier', 'valid_from', 'valid_to',
            'fixed', 'peak', 'rest', 'valley', 'power'
        )
