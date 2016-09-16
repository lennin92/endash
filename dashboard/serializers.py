from dashboard.models import Measure, Node
from rest_framework import serializers


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('id', 'url', 'padre', 'nombre', 'coordenada',
                  'descripcion', 'hijos', 'fotografia', 'demandas')


class MeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Measure
        fields =('node', 'datetime', 'datetime_int', 'active',
                 'apparent', 'demand')
